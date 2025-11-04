import React from 'react';
import { 
  Box, 
  Typography, 
  Card, 
  CardContent, 
  Accordion, 
  AccordionSummary, 
  AccordionDetails,
  List,
  ListItem,
  ListItemText,
  Link,
  Divider,
  CircularProgress,
  useMediaQuery,
  useTheme,
  IconButton,
  CardMedia,
  Grid
} from '@mui/material';
import YouTubeIcon from '@mui/icons-material/YouTube';

const AnimeList = ({ animeData, loading }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (!animeData || animeData.length === 0) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography variant="h6">没有找到动漫数据</Typography>
      </Box>
    );
  }

  // 平台链接构造函数，便于后续扩展其他平台
  const buildLink = (platform, payload) => {
    if (!payload) return null;
    switch (platform) {
      case 'youtube': {
        // 允许 payload 为对象 { videoId } 或字符串完整URL
        if (typeof payload === 'string') {
          return payload.startsWith('http') ? payload : `https://www.youtube.com/watch?v=${payload}`;
        }
        const id = payload.videoId || payload.id;
        if (!id) return null;
        return `https://www.youtube.com/watch?v=${id}`;
      }
      default:
        return null;
    }
  };

  const PlatformIcons = ({ item }) => {
    const icons = [];
    // 当前仅支持 YouTube，未来可在此处扩展更多平台
    const ytLink = buildLink('youtube', item.youtube);
    if (ytLink) {
      icons.push(
        <IconButton key="youtube" component="a" href={ytLink} target="_blank" rel="noopener noreferrer" size="medium" aria-label="YouTube" sx={{ p: 0.5 }}>
          <YouTubeIcon color="error" sx={{ fontSize: 22 }} />
        </IconButton>
      );
    }
    return icons.length ? <Box sx={{ display: 'flex', gap: 1, flexShrink: 0 }}>{icons}</Box> : null;
  };

  return (
    <Box sx={{ width: '100%' }}>
      <Typography variant="h4" gutterBottom sx={{ fontSize: { xs: '1.5rem', md: '2.125rem' } }}>
        动漫列表
      </Typography>
      <Box 
        sx={{ 
          display: 'grid',
          gridTemplateColumns: { xs: '1fr', sm: 'repeat(2, 1fr)', md: 'repeat(3, 1fr)' },
          gap: 2
        }}
      >
        {animeData.map((anime, index) => (
          <Card key={index} sx={{ overflow: 'visible' }}>
            <CardContent sx={{ p: { xs: 2, md: 3 } }}>
              <Box 
                sx={{ 
                  display: 'grid', 
                  gridTemplateColumns: { xs: '1fr', md: 'auto 1fr' },
                  columnGap: 2,
                  rowGap: { xs: 2, md: 0 },
                  alignItems: 'start'
                }}
              >
                {/* 左侧：封面图 + 名称 */}
                <Box sx={{ width: { xs: 120, md: 160 } }}>
                  {anime.pic && (
                    <CardMedia
                      component="img"
                      image={anime.pic}
                      alt={anime.cn_name || ''}
                      sx={{ 
                        width: { xs: 120, md: 160 },
                        height: { xs: 120, md: 160 },
                        objectFit: 'contain',
                        objectPosition: 'center',
                        bgcolor: '#fff',
                        borderRadius: 1,
                        display: 'block',
                        ml: 0
                      }}
                      referrerPolicy="no-referrer"
                      loading="lazy"
                      onError={(e) => { e.currentTarget.src = '/logo192.png'; }}
                    />
                  )}
                  <Typography 
                    variant="subtitle1" 
                    sx={{ mt: 1, fontWeight: 600, fontSize: { xs: '0.95rem', md: '1rem' }, textAlign: 'center', wordBreak: 'break-word', overflowWrap: 'break-word', whiteSpace: 'normal', hyphens: 'auto', maxWidth: '100%' }}
                  >
                    {anime.cn_name || anime.animate_name}
                  </Typography>
                </Box>

                {/* 右侧：OP/ED 列表 */}
                <Box sx={{ mt: { xs: 2, md: 0 }, minWidth: { xs: 0, md: 240 } }}>
                  {/* OP列表 */}
                  <Accordion sx={{ mt: 0 }}>
                    <AccordionSummary
                      expandIcon={<span>▼</span>}
                      aria-controls="op-content"
                      id={`op-header-${index}`}
                    >
                      <Typography sx={{ display: 'flex', alignItems: 'center' }}>
                        <span style={{ marginRight: '8px' }}>♪</span> OP列表
                      </Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                      <List dense>
                        {(anime.op || []).map((opItem, opIndex) => (
                          <React.Fragment key={opIndex}>
                            <ListItem secondaryAction={<PlatformIcons item={opItem} />} sx={{ alignItems: 'flex-start', pr: { xs: 7, md: 8 } }}> 
                              <ListItemText 
                                primary={opItem.text || '未命名OP'}
                                secondary={opItem.ep_id && opItem.ep_id !== -1 ? String(opItem.ep_id) : null}
                                primaryTypographyProps={{ sx: { wordBreak: 'normal', overflowWrap: 'break-word', whiteSpace: 'normal' } }}
                              />
                            </ListItem>
                            {opIndex < (anime.op || []).length - 1 && <Divider />}
                          </React.Fragment>
                        ))}
                      </List>
                    </AccordionDetails>
                  </Accordion>

                  {/* ED列表 */}
                  <Accordion sx={{ mt: 1 }}>
                    <AccordionSummary
                      expandIcon={<span>▼</span>}
                      aria-controls="ed-content"
                      id={`ed-header-${index}`}
                    >
                      <Typography sx={{ display: 'flex', alignItems: 'center' }}>
                        <span style={{ marginRight: '8px' }}>♪</span> ED列表
                      </Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                      <List dense>
                        {(anime.ed || []).map((edItem, edIndex) => (
                          <React.Fragment key={edIndex}>
                            <ListItem secondaryAction={<PlatformIcons item={edItem} />} sx={{ alignItems: 'flex-start', pr: { xs: 7, md: 8 } }}>
                              <ListItemText 
                                primary={edItem.text || '未命名ED'}
                                secondary={edItem.ep_id && edItem.ep_id !== -1 ? String(edItem.ep_id) : null}
                                primaryTypographyProps={{ sx: { wordBreak: 'normal', overflowWrap: 'break-word', whiteSpace: 'normal' } }}
                              />
                            </ListItem>
                            {edIndex < (anime.ed || []).length - 1 && <Divider />}
                          </React.Fragment>
                        ))}
                      </List>
                    </AccordionDetails>
                  </Accordion>
                </Box>
              </Box>
            </CardContent>
          </Card>
        ))}
      </Box>
    </Box>
  );
};

export default AnimeList;