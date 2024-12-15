import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const KnowledgePopup = ({ node, onClose, isVisible, dimensions }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [isClosing, setIsClosing] = useState(false);

  if (!node) return null;

  const handleClose = () => {
    setIsClosing(true);
    setTimeout(() => {
      setIsClosing(false);
      onClose();
    }, 500);
  };

  const renderContent = (label, content) => {
    if (!content || (Array.isArray(content) && content.length === 0)) return null;
    return (
      <div className="content-section" style={{ marginBottom: '20px' }}>
        <h3 style={{ 
          fontSize: '1.2em', 
          fontWeight: 'bold',
          marginBottom: '10px',
          color: '#e0e0e0'
        }}>{label}</h3>
        {Array.isArray(content) ? (
          <p style={{ color: '#e0e0e0' }}>{content.join(', ')}</p>
        ) : (
          <p style={{ 
            color: '#e0e0e0',
            whiteSpace: 'pre-wrap'
          }}>{content}</p>
        )}
      </div>
    );
  };

  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{ x: '160%' }}
          animate={{ 
            x: isClosing ? '160%' : 0,
          }}
          exit={{ x: '160%' }}
          transition={{ 
            type: "spring",
            stiffness: 150,
            damping: 25,
            mass: 1.3,
            delay: isClosing ? 0 : 0.5
          }}
          style={{
            position: 'fixed',
            top: '19%',
            left: '40%',
            marginLeft: '16rem',
          }}
        >
          <button 
            onClick={handleClose}
            className="absolute -top-28 left-1/2 -translate-x-1/2 z-50 bg-gray-400 hover:bg-black text-white rounded-full w-14 h-14 flex items-center justify-center shadow-lg"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>

          <motion.div
            style={{ 
              width: dimensions.width,
              height: dimensions.height,
              borderRadius: '30%',
              overflow: 'hidden',
              backgroundColor: '#000003',
              boxShadow: '0 0 50px rgba(0, 0, 0, 0.5)'
            }}
            className="relative"
          >
            <div className="absolute inset-0 px-8 pb-8 overflow-y-auto text-white popup-content" style={{ 
              msOverflowStyle: 'none', 
              scrollbarWidth: 'none'
            }}>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="text-center mt-8"
              >
                <h2 className="text-4xl font-bold mb-8">{node.name}</h2>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
                className="mb-8"
              >
                {renderContent('태그', node.tags)}
              </motion.div>

              {node.summary && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.5 }}
                  className="mb-8"
                >
                  {renderContent('요약', node.summary)}
                </motion.div>
              )}

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6 }}
                className="mb-8"
              >
                {renderContent('내용', node.content)}
              </motion.div>

              {node.references && node.references.length > 0 && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.7 }}
                  className="mb-8"
                >
                  {renderContent('참고 자료', node.references)}
                </motion.div>
              )}
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default KnowledgePopup;
