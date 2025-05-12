import React, { useState, useEffect } from 'react';
import { ThreeDots } from 'react-loader-spinner';
import DocumentCard from '../components/documents/DocumentCard';
import Pagination from '../components/common/Pagination';
import { fetchDocuments } from '../services/Api.js';

export default function DocumentList() {
  const [documents, setDocuments] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadDocuments = async () => {
      try {
        const response = await fetchDocuments(currentPage);
        setDocuments(response.data.data);
        setTotalPages(Math.ceil(response.data.pagination.total / 10));
      } finally {
        setLoading(false);
      }
    };
    loadDocuments();
  }, [currentPage]);

  return (
    <div className="pt-24 px-4 max-w-7xl mx-auto">
      <h2 className="text-3xl font-bold text-gray-900 mb-8">Your Documents</h2>
      
      {loading ? (
        <div className="flex justify-center">
          <ThreeDots color="#4F46E5" height={50} width={50} />
        </div>
      ) : (
        <>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {documents.map((doc) => (
              <DocumentCard key={doc.id} document={doc} />
            ))}
          </div>
          
          <Pagination 
            currentPage={currentPage}
            totalPages={totalPages}
            onPageChange={setCurrentPage}
          />
        </>
      )}
    </div>
  );
}