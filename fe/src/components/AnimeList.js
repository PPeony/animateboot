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
  useTheme
} from '@mui/material';

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

  return (
    <Box sx={{ width: '100%' }}>
      <Typography variant="h4" gutterBottom sx={{ fontSize: { xs: '1.5rem', md: '2.125rem' } }}>
        动漫列表
      </Typography>
      {animeData.map((anime, index) => (
        <Card key={index} sx={{ mb: 2 }}>
          <CardContent sx={{ p: { xs: 2, md: 3 } }}>
            <Typography variant="h5" component="div" sx={{ fontSize: { xs: '1.25rem', md: '1.5rem' } }}>
              {anime.animate_name}
            </Typography>
            
            {/* OP列表 */}
            <Accordion sx={{ mt: 2 }}>
              <AccordionSummary
                expandIcon={<span>▼</span>}
                aria-controls="op-content"
                id="op-header"
              >
                <Typography sx={{ display: 'flex', alignItems: 'center' }}>
                  <span style={{ marginRight: '8px' }}>♪</span> OP列表
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <List>
                  {anime.op.map((op, opIndex) => {
                    // 获取OP的键名和值
                    const opKey = Object.keys(op).find(key => key.startsWith('op'));
                    const linkKey = Object.keys(op).find(key => key.startsWith('link'));
                    
                    return (
                      <React.Fragment key={opIndex}>
                        <ListItem>
                          <ListItemText 
                            primary={op[opKey]} 
                            secondary={
                              <Link href={op[linkKey]} target="_blank" rel="noopener noreferrer">
                                查看链接
                              </Link>
                            }
                          />
                        </ListItem>
                        {opIndex < anime.op.length - 1 && <Divider />}
                      </React.Fragment>
                    );
                  })}
                </List>
              </AccordionDetails>
            </Accordion>
            
            {/* ED列表 */}
            <Accordion sx={{ mt: 1 }}>
              <AccordionSummary
                expandIcon={<span>▼</span>}
                aria-controls="ed-content"
                id="ed-header"
              >
                <Typography sx={{ display: 'flex', alignItems: 'center' }}>
                  <span style={{ marginRight: '8px' }}>♪</span> ED列表
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <List>
                  {anime.ed.map((ed, edIndex) => {
                    // 获取ED的键名和值
                    const edKey = Object.keys(ed).find(key => key.startsWith('ed'));
                    const linkKey = Object.keys(ed).find(key => key.startsWith('link'));
                    
                    return (
                      <React.Fragment key={edIndex}>
                        <ListItem>
                          <ListItemText 
                            primary={ed[edKey]} 
                            secondary={
                              <Link href={ed[linkKey]} target="_blank" rel="noopener noreferrer">
                                查看链接
                              </Link>
                            }
                          />
                        </ListItem>
                        {edIndex < anime.ed.length - 1 && <Divider />}
                      </React.Fragment>
                    );
                  })}
                </List>
              </AccordionDetails>
            </Accordion>
          </CardContent>
        </Card>
      ))}
    </Box>
  );
};

export default AnimeList;