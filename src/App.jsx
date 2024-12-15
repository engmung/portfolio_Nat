import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import {
  ThemeProvider,
  createTheme,
  AppBar,
  Toolbar,
  Button,
  Box,
  CssBaseline,
} from '@mui/material';
import KnowledgeGraph from './components/KnowledgeGraph';
import KnowledgeFileManager from './components/KnowledgeFileManager';
import AISearchBar from './components/AISearchBar';
import AIResponsePopup from './components/AIResponsePopup';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const theme = createTheme({
  palette: {
    mode: 'dark',
  },
});

const App = () => {
  const [aiPopupOpen, setAiPopupOpen] = useState(false);
  const [aiResponse, setAiResponse] = useState('');

  const handleAISearch = async (query) => {
    try {
      const response = await fetch(`${API_URL}/ai/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });
      const data = await response.json();
      setAiResponse(data.response);
      setAiPopupOpen(true);
    } catch (error) {
      console.error('Error:', error);
      setAiResponse('Error occurred while processing your request.');
      setAiPopupOpen(true);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ flexGrow: 1 }}>
          <AppBar position="static">
            <Toolbar>
              <Button
                component={Link}
                to="/"
                color="inherit"
                sx={{ mr: 2 }}
              >
                Knowledge Graph
              </Button>
              <Button
                component={Link}
                to="/manage"
                color="inherit"
              >
                Knowledge Manager
              </Button>
            </Toolbar>
          </AppBar>

          <Box sx={{ p: 3 }}>
            <Routes>
              <Route
                path="/"
                element={
                  <Box sx={{ position: 'relative', height: 'calc(100vh - 128px)' }}>
                    <KnowledgeGraph />
                    <Box sx={{ position: 'absolute', top: 16, left: 16, right: 16 }}>
                      <AISearchBar onSubmit={handleAISearch} />
                    </Box>
                    <AIResponsePopup
                      open={aiPopupOpen}
                      onClose={() => setAiPopupOpen(false)}
                      response={aiResponse}
                    />
                  </Box>
                }
              />
              <Route path="/manage" element={<KnowledgeFileManager />} />
            </Routes>
          </Box>
        </Box>
      </Router>
    </ThemeProvider>
  );
};

export default App;
