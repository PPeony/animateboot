// import axios from 'axios';

// 基础URL，实际开发中应该从环境变量获取
const BASE_URL = 'http://your-api-url.com/api';

// Mock数据
const mockSeasons = [];
for (let year = 2020; year <= 2025; year++) {
  [1, 4, 7, 10].forEach(month => {
    mockSeasons.push({ year, month });
  });
}

const mockAnimeData = {
  '2020-1': [
    {
      animate_name: '冬季番剧1',
      op: [
        { op1: '冬季OP1', link1: 'https://example.com/2020-1-op1' }
      ],
      ed: [
        { ed1: '冬季ED1', link1: 'https://example.com/2020-1-ed1' }
      ]
    }
  ],
  '2020-4': [
    {
      animate_name: '春季番剧1',
      op: [
        { op1: '春季OP1', link1: 'https://example.com/2020-4-op1' }
      ],
      ed: [
        { ed1: '春季ED1', link1: 'https://example.com/2020-4-ed1' }
      ]
    }
  ],
  // 添加更多季度的数据...
  '2025-1': [
    {
      animate_name: '2025冬季番剧',
      op: [
        { op1: '2025冬季OP1', link1: 'https://example.com/2025-1-op1' },
        { op2: '2025冬季OP2', link1: 'https://example.com/2025-1-op2' }
      ],
      ed: [
        { ed1: '2025冬季ED1', link1: 'https://example.com/2025-1-ed1' }
      ]
    },
    {
      animate_name: '2025冬季番剧2',
      op: [
        { op1: '2025冬季2-OP1', link1: 'https://example.com/2025-1-2-op1' }
      ],
      ed: [
        { ed1: '2025冬季2-ED1', link1: 'https://example.com/2025-1-2-ed1' },
        { ed2: '2025冬季2-ED2', link1: 'https://example.com/2025-1-2-ed2' }
      ]
    }
  ]
};

// 获取所有可用季度
export const getSeasons = async () => {
  try {
    // 实际API调用
    // const response = await axios.get(`${BASE_URL}/seasons`);
    // return response.data;
    
    // 使用Mock数据
    return mockSeasons;
  } catch (error) {
    console.error('获取季度数据失败:', error);
    throw error;
  }
};

// 获取特定季度的动漫数据
export const getAnimeData = async (year, month) => {
  try {
    // 实际API调用
    // const response = await axios.get(`${BASE_URL}/anime?year=${year}&month=${month}`);
    // return response.data;
    
    // 使用Mock数据
    const key = `${year}-${month}`;
    // 如果没有该季度的数据，返回一个默认数据
    return mockAnimeData[key] || [
      {
        animate_name: `animate1`,
        op: [
          { op1: `${year}-${month} OP1`, link1: `https://example.com/${year}-${month}-op1` }
        ],
        ed: [
          { ed1: `${year}-${month} ED1`, link1: `https://example.com/${year}-${month}-ed1` }
        ]
      },
      {
        animate_name: `animate2`,
        op: [
          { op1: `${year}-${month} OP1`, link1: `https://example.com/${year}-${month}-op1` }
        ],
        ed: [
          { ed1: `${year}-${month} ED1`, link1: `https://example.com/${year}-${month}-ed1` }
        ]
      }
    ];
  } catch (error) {
    console.error('获取动漫数据失败:', error);
    throw error;
  }
};