import React, { useState, useEffect } from 'react';
import { 
  Drawer, 
  List, 
  ListItem, 
  ListItemButton, 
  ListItemText, 
  Typography, 
  Divider,
  Box,
  useMediaQuery,
  IconButton,
  SwipeableDrawer
} from '@mui/material';
import { styled, useTheme } from '@mui/material/styles';
import { getSeasons } from '../services/api';


// 侧边栏宽度
const drawerWidth = 240;

// 自定义样式
const StyledDrawer = styled(Drawer)(({ theme }) => ({
  width: drawerWidth,
  flexShrink: 0,
  '& .MuiDrawer-paper': {
    width: drawerWidth,
    boxSizing: 'border-box',
  },
}));

const Sidebar = ({ onSeasonSelect, selectedSeason }) => {
  const [seasons, setSeasons] = useState([]);
  const [mobileOpen, setMobileOpen] = useState(false);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  useEffect(() => {
    // 获取季度数据
    const fetchSeasons = async () => {
      try {
        const data = await getSeasons();
        setSeasons(data);
      } catch (error) {
        console.error('获取季度数据失败:', error);
        // 使用模拟数据作为备选
        const mockSeasons = [];
        for (let year = 2020; year <= 2025; year++) {
          [1, 4, 7, 10].forEach(month => {
            mockSeasons.push({ year, month });
          });
        }
        setSeasons(mockSeasons);
      }
    };
    
    fetchSeasons();
  }, []);

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

  // 检查是否为当前选中的季度
  const isSelected = (season) => {
    return selectedSeason && 
           selectedSeason.year === season.year && 
           selectedSeason.month === season.month;
  };

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleSeasonClick = (season) => {
    onSeasonSelect(season);
    if (isMobile) {
      setMobileOpen(false);
    }
  };

  const drawerContent = (
    <>
      <Box sx={{ p: 2, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Typography variant="h6" noWrap component="div">
          动漫季度
        </Typography>
        {isMobile && (
          <IconButton onClick={handleDrawerToggle}>
            <span>☰</span>
          </IconButton>
        )}
      </Box>
      <Divider />
      <List sx={{ overflow: 'auto' }}>
        {seasons.map((season, index) => (
          <ListItem key={index} disablePadding>
            <ListItemButton 
              selected={isSelected(season)}
              onClick={() => handleSeasonClick(season)}
            >
              <ListItemText 
                primary={`${season.year}年 ${getSeasonName(season.month)}`} 
              />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </>
  );

  return (
    <>
      {isMobile && (
        <IconButton
          color="inherit"
          aria-label="open drawer"
          edge="start"
          onClick={handleDrawerToggle}
          sx={{ mr: 2, position: 'absolute', top: 10, left: 10, zIndex: 1100 }}
        >
          <span>☰</span>
        </IconButton>
      )}
      
      {isMobile ? (
        <SwipeableDrawer
          open={mobileOpen}
          onClose={handleDrawerToggle}
          onOpen={handleDrawerToggle}
          sx={{
            '& .MuiDrawer-paper': { width: drawerWidth, boxSizing: 'border-box' },
          }}
        >
          {drawerContent}
        </SwipeableDrawer>
      ) : (
        <StyledDrawer variant="permanent" anchor="left">
          {drawerContent}
        </StyledDrawer>
      )}
    </>
  );
};

export default Sidebar;