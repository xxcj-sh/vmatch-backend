// API 配置
const API_CONFIG = {
  baseURL: 'http://localhost:8000/api/v1', // 仅在非测试模式下使用
  timeout: 10000,
  retryCount: 3
};

// 存储相关
const STORAGE_KEYS = {
  TOKEN: 'token',
  USER_INFO: 'user_info',
  EXPIRES_IN: 'expires_in'
};

module.exports = {
  API_CONFIG,
  STORAGE_KEYS
};