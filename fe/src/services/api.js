// import axios from 'axios';

// 基础URL，实际开发中应该从环境变量获取
// const BASE_URL = process.env.REACT_APP_API_URL;

// 使用Webpack的require.context来自动发现并加载季度数据文件
// 数据文件位于 src/data 目录，命名为 6位年月：YYYYMM.json
const seasonsContext = require.context('../data', false, /^\.\/\d{6}\.json$/);

// 从文件名解析出 { year, month }
const parseSeasonFilename = (filename) => {
  const base = filename.replace('./', '').replace('.js', '');
  const year = Number(base.slice(0, 4));
  const month = Number(base.slice(4, 6));
  return { year, month, key: base };
};

// 获取所有可用季度（依据目录中的文件名）
export const getSeasons = async () => {
  try {
    const seasons = seasonsContext
      .keys()
      .map(parseSeasonFilename)
      .sort((a, b) => (b.year - a.year) || (b.month - a.month));
    return seasons;
  } catch (error) {
    console.error('获取季度数据失败:', error);
    return [];
  }
};

// 获取特定季度的动漫数据（按文件名加载）
export const getAnimeData = async (year, month) => {
  try {
    const key = `${year}${String(month).padStart(2, '0')}`; // e.g., 202501
    const raw = seasonsContext(`./${key}.json`);
    const data = raw && raw.default ? raw.default : raw; // 兼容不同打包行为
    return Array.isArray(data) ? data : [];
  } catch (error) {
    console.warn(`未找到季度数据文件: ${year}-${month}`, error);
    return [];
  }
};