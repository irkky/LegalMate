import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { FiTrash2, FiFileText, FiAlertTriangle } from 'react-icons/fi';
import { ThreeDots } from 'react-loader-spinner';
import { fetchDocument, deleteDocument } from '../services/Api';
import AnalysisSection from '../components/common/AnalysisSection';
import RiskChart from '../components/documents/RiskChart';
import EntityVisualization from '../components/documents/EntityVisualization';

class ErrorBoundary extends React.Component {
  state = { hasError: false, error: null };
  
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }
  
  componentDidCatch(error, errorInfo) {
    console.error('Component Error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="p-4 bg-red-50 text-red-600 rounded-lg">
          <h3>Component Error:</h3>
          <pre>{this.state.error.toString()}</pre>
        </div>
      );
    }
    return this.props.children;
  }
}

export default function DocumentDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [document, setDocument] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;

    const loadDocument = async () => {
      try {
        console.log('Fetching document ID:', id);
        const response = await fetchDocument(id);
        console.log('API Response:', response);
        
        // Extract nested data from Axios response
        const documentData = response.data;
        console.log('Document Data:', {
          id: documentData?.id,
          text: documentData?.text?.length,
          analysis: documentData?.analysis ? {
            summary: documentData.analysis.summary?.length,
            risks: documentData.analysis.risks?.length,
            entities: documentData.analysis.entities 
              ? Object.keys(documentData.analysis.entities).length 
              : 0
          } : null
        });

        if (!documentData?.id) {
          throw new Error('Invalid document data structure');
        }

        setDocument(documentData);
      } catch (error) {
        console.error('Document load error:', {
          message: error.message,
          response: error.response?.data
        });
        navigate('/documents');
      } finally {
        setLoading(false);
      }
    };

    loadDocument();
  }, [id, navigate]);

  const handleDeleteDocument = async () => {
    if (window.confirm('Are you sure you want to delete this document?')) {
      try {
        await deleteDocument(id);
        navigate('/documents');
      } catch (error) {
        console.error('Delete failed:', {
          status: error.response?.status,
          data: error.response?.data
        });
      }
    }
  };

  console.log('Current Document State:', {
    id: document?.id,
    hasText: !!document?.text,
    hasAnalysis: !!document?.analysis,
    risks: document?.analysis?.risks?.length || 0,
    entities: document?.analysis?.entities 
      ? Object.keys(document.analysis.entities).length 
      : 0
  });

  if (loading) {
    return (
      <div className="pt-24 flex justify-center">
        <ThreeDots color="#4F46E5" height={50} width={50} />
      </div>
    );
  }

  if (!document) {
    return (
      <div className="pt-24 text-center text-red-500">
        Document not found or failed to load
      </div>
    );
  }

  return (
    <ErrorBoundary>
      <div className="pt-24 px-4 max-w-7xl mx-auto">
        <div className="flex justify-between items-start mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              {document.filename}
            </h1>
            <p className="text-gray-500 mt-2">
              Uploaded: {new Date(document.upload_date).toLocaleDateString()}
            </p>
          </div>
          <button 
            className="bg-red-100 text-red-600 px-4 py-2 rounded-lg hover:bg-red-200 flex items-center"
            onClick={handleDeleteDocument}
            aria-label="Delete document"
          >
            <FiTrash2 className="mr-2" /> Delete Document
          </button>
        </div>

        <div className="grid gap-8 md:grid-cols-2">
          <AnalysisSection 
            title="Document Summary" 
            icon={<FiFileText />}
            content={document.analysis?.summary || 'No summary available'}
          />

          <ErrorBoundary>
            <AnalysisSection 
              title="Identified Risks" 
              icon={<FiAlertTriangle />}
              content={
                document.analysis?.risks?.length > 0 ? (
                  <RiskChart risks={document.analysis.risks} />
                ) : 'No risks identified'
              }
            />
          </ErrorBoundary>

          {document.analysis?.entities && (
            <ErrorBoundary>
              <EntityVisualization entities={document.analysis.entities} />
            </ErrorBoundary>
          )}

          <div className="bg-white rounded-xl p-6 shadow-sm">
            <h3 className="text-xl font-semibold mb-4">Full Text</h3>
            <div className="prose max-h-96 overflow-y-auto whitespace-pre-wrap">
              {document.text || (
                <div className="text-gray-400 text-sm">
                  <p>Text content not available</p>
                  <ul className="list-disc pl-4 mt-2">
                    <li>Document might still be processing</li>
                    <li>Text extraction might have failed</li>
                    <li>Unsupported file format</li>
                  </ul>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </ErrorBoundary>
  );
}