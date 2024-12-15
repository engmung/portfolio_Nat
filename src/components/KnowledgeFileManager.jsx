import React, { useState, useEffect } from 'react';

const KnowledgeFileManager = () => {
  const [knowledgeFiles, setKnowledgeFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [message, setMessage] = useState({ text: '', type: '' });

  const fetchKnowledgeFiles = async () => {
    try {
      const response = await fetch('http://localhost:8000/knowledge/files');
      if (!response.ok) {
        throw new Error('Failed to fetch knowledge files');
      }
      const data = await response.json();
      setKnowledgeFiles(data.files);  // 응답에서 files 배열을 추출
    } catch (error) {
      console.error('Error fetching knowledge files:', error);
      setMessage({ text: '파일 목록을 불러오는데 실패했습니다.', type: 'error' });
    }
  };

  useEffect(() => {
    fetchKnowledgeFiles();
  }, []);

  const handleFileSelect = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setMessage({ text: '파일을 선택해주세요', type: 'error' });
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('http://localhost:8000/knowledge/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('업로드 실패');
      setMessage({ text: '업로드 성공', type: 'success' });
      fetchKnowledgeFiles();
    } catch (error) {
      setMessage({ text: '업로드 실패: ' + error.message, type: 'error' });
    }
  };

  const handleDownload = async (filename) => {
    try {
      const response = await fetch(
        `http://localhost:8000/knowledge/download/${filename}`
      );
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);

      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      setMessage({ text: '다운로드 실패: ' + error.message, type: 'error' });
    }
  };

  const handleDelete = async (filename) => {
    if (!confirm('정말 삭제하시겠습니까?')) return;
    
    try {
      const response = await fetch(`http://localhost:8000/knowledge/files/${filename}`, {
        method: 'DELETE'
      });
      if (!response.ok) throw new Error('삭제 실패');
      setMessage({ text: '삭제 성공', type: 'success' });
      fetchKnowledgeFiles();
    } catch (error) {
      setMessage({ text: '삭제 실패: ' + error.message, type: 'error' });
    }
  };

  const handleRebuild = async () => {
    try {
      const response = await fetch('http://localhost:8000/knowledge/rebuild', {
        method: 'POST'
      });
      if (!response.ok) throw new Error('재구축 실패');
      setMessage({ text: '데이터베이스 재구축 성공', type: 'success' });
      fetchKnowledgeFiles();
    } catch (error) {
      setMessage({ text: '데이터베이스 재구축 실패: ' + error.message, type: 'error' });
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <div style={{ marginBottom: '20px' }}>
        <input
          type="file"
          accept=".yaml"
          onChange={handleFileSelect}
          style={{ marginRight: '10px' }}
        />
        <button 
          onClick={handleUpload} 
          style={{ 
            marginRight: '10px',
            backgroundColor: '#4CAF50',
            color: 'white',
            padding: '8px 16px',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          업로드
        </button>
        <button 
          onClick={handleRebuild} 
          style={{ 
            marginRight: '10px',
            backgroundColor: '#2196F3',
            color: 'white',
            padding: '8px 16px',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          DB 재구축
        </button>
        <button 
          onClick={() => window.location.href = 'http://localhost:8000/knowledge/template'}
          style={{ 
            backgroundColor: '#9C27B0',
            color: 'white',
            padding: '8px 16px',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          템플릿 다운로드
        </button>
      </div>

      {message.text && (
        <div style={{ margin: '10px 0', color: message.type === 'error' ? 'red' : 'green' }}>
          {message.text}
        </div>
      )}

      {selectedFile && (
        <div style={{ margin: '10px 0' }}>
          선택된 파일: {selectedFile.name}
        </div>
      )}

      <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '20px' }}>
        <thead>
          <tr>
            <th style={{ padding: '12px',  borderBottom: '2px solid #ddd' }}>제목</th>
            <th style={{ padding: '12px',  borderBottom: '2px solid #ddd' }}>레벨</th>
            <th style={{ padding: '12px',  borderBottom: '2px solid #ddd' }}>태그</th>
            <th style={{ padding: '12px',  borderBottom: '2px solid #ddd' }}>파일명</th>
            <th style={{ padding: '12px',  borderBottom: '2px solid #ddd' }}>작업</th>
          </tr>
        </thead>
        <tbody>
          {knowledgeFiles.map((file, index) => (
            <tr key={index}>
              <td style={{ padding: '12px', borderBottom: '1px solid #ddd' }}>{file.title}</td>
              <td style={{ padding: '12px', borderBottom: '1px solid #ddd' }}>{file.level}</td>
              <td style={{ padding: '12px', borderBottom: '1px solid #ddd' }}>{file.tags.join(', ')}</td>
              <td style={{ padding: '12px', borderBottom: '1px solid #ddd' }}>{file.filename}</td>
              <td style={{ padding: '12px', borderBottom: '1px solid #ddd' }}>
                <button 
                  onClick={() => handleDownload(file.filename)} 
                  style={{ 
                    marginRight: '5px',
                    backgroundColor: '#2196F3',
                    color: 'white',
                    padding: '6px 12px',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer'
                  }}
                >
                  다운로드
                </button>
                <button 
                  onClick={() => handleDelete(file.filename)}
                  style={{ 
                    backgroundColor: '#f44336',
                    color: 'white',
                    padding: '6px 12px',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer'
                  }}
                >
                  삭제
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default KnowledgeFileManager;
