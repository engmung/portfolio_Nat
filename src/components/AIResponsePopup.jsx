import React from 'react';

const AIResponsePopup = ({ open, onClose, response }) => {
  if (!response || !open) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-gray-900 rounded-lg w-full max-w-3xl max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h2 className="text-xl font-bold text-white">AI Response</h2>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-white"
            >
              ✕
            </button>
          </div>

          <div className="mb-6">
            <p className="text-gray-300 whitespace-pre-wrap">
              {response}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIResponsePopup;
