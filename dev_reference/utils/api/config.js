// API 配置
const { getCurrentEnvConfig } = require('./env');

const envConfig = getCurrentEnvConfig();

const API_CONFIG = {
  baseURL: envConfig.baseURL,
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