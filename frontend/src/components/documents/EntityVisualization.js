import React from 'react';

export default function EntityVisualization({ entities }) {
  return (
    <div className="bg-white rounded-xl p-6 shadow-sm">
      <h3 className="text-xl font-semibold mb-4">Entities & Clauses</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {Object.entries(entities).map(([type, values]) => (
          <div key={type} className="bg-indigo-50 p-4 rounded-lg">
            <h4 className="font-medium text-indigo-700">{type}</h4>
            <ul className="mt-2 space-y-1">
              {values.slice(0, 5).map((value, index) => (
                <li 
                  key={index} 
                  className="text-indigo-600 truncate"
                  title={value}
                >
                  {value}
                </li>
              ))}
              {values.length > 5 && (
                <li className="text-indigo-400 text-sm">
                  + {values.length - 5} more...
                </li>
              )}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}