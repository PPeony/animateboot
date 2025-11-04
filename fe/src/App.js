import React, { useState, useEffect } from 'react';
import { Box, CssBaseline, ThemeProvider, createTheme, Typography, useMediaQuery } from '@mui/material';
import './App.css';
import Sidebar from './components/Sidebar';
import AnimeList from './components/AnimeList';
import { getAnimeData, getSeasons } from './services/api';

// 创建主题
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  const [selectedSeason, setSelectedSeason] = useState(null);
  const [animeData, setAnimeData] = useState([]);
  const [loading, setLoading] = useState(true);

  // 默认加载最新的季度（依据数据文件倒序）
  useEffect(() => {
    const initSeason = async () => {
      try {
        const seasons = await getSeasons();
        if (seasons && seasons.length > 0) {
          setSelectedSeason(seasons[0]);
        }
      } catch (e) {
        console.error('初始化季度失败', e);
      }
    };
    initSeason();
  }, []);

  // 当选中的季度变化时，获取相应的动漫数据
  useEffect(() => {
    if (selectedSeason) {
      fetchAnimeData(selectedSeason);
    }
  }, [selectedSeason]);

  // 获取动漫数据的函数
  const fetchAnimeData = async (season) => {
    setLoading(true);
    try {
      // 调用API服务获取数据
      const data = await getAnimeData(season.year, season.month);
      console.log('获取到的动漫数据:', data); // 添加调试信息
      setAnimeData(data);
    } catch (error) {
      console.error('获取动漫数据失败:', error);
      // 发生错误时设置空数据
      setAnimeData([]);
    } finally {
      setLoading(false);
    }
  };

  // 处理季度选择
  const handleSeasonSelect = (season) => {
    setSelectedSeason(season);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: 'flex', height: '100vh', flexDirection: { xs: 'column', md: 'row' } }}>
        <Sidebar onSeasonSelect={handleSeasonSelect} selectedSeason={selectedSeason} />
        <Box component="main" sx={{ 
          flexGrow: 1, 
          p: 3, 
          mt: { xs: 5, md: 0 },
          width: { xs: '100%', md: 'auto' }
        }}>
          {selectedSeason && (
            <Box sx={{ mb: 2 }}>
              <Typography variant="h6" color="primary">
                {selectedSeason.year}年 {getSeasonName(selectedSeason.month)}季度
              </Typography>
            </Box>
          )}
          <AnimeList animeData={animeData} loading={loading} />
        </Box>
      </Box>
    </ThemeProvider>
  );
}

// 获取季度的显示名称
const getSeasonName = (month) => {
  switch (month) {
    case 1: return '一月';
    case 4: return '四月';
    case 7: return '七月';
    case 10: return '十月';
    default: return '';
  }
};

export default App;
