// 统一API入口文件
const AuthAPI = require('./auth');
const UserAPI = require('./user');
const MatchingAPI = require('./matching');
const ChatAPI = require('./chat');
const MembershipAPI = require('./membership');
const { baseURL, API_TIMEOUT, API_RETRY_COUNT, STORAGE_KEYS } = require('./config');

// 创建各模块实例
const authAPI = new AuthAPI();
const userAPI = new UserAPI();
const matchingAPI = new MatchingAPI();
const chatAPI = new ChatAPI();
const membershipAPI = new MembershipAPI();

// 向后兼容：导出原有方法
module.exports = {
  // 配置
  baseURL,
  API_TIMEOUT,
  API_RETRY_COUNT,
  STORAGE_KEYS,
  
  // 认证相关方法
  wxLogin: authAPI.wxLogin.bind(authAPI),
  phoneLogin: authAPI.phoneLogin.bind(authAPI),
  sendVerificationCode: authAPI.sendVerificationCode.bind(authAPI),
  register: authAPI.register.bind(authAPI),
  logout: authAPI.logout.bind(authAPI),
  validateToken: authAPI.validateToken.bind(authAPI),
  
  // 用户相关方法
  getUserInfo: userAPI.getUserInfo.bind(userAPI),
  getProfile: userAPI.getProfile.bind(userAPI),
  getOtherUserProfile: userAPI.getOtherUserProfile.bind(userAPI),
  updateProfile: userAPI.updateProfile.bind(userAPI),
  getUserFullProfile: userAPI.getUserFullProfile.bind(userAPI),
  updateUserProfile: userAPI.updateUserProfile.bind(userAPI),
  getUserStats: userAPI.getUserStats.bind(userAPI),
  
  // 匹配相关方法
  getMatchCards: matchingAPI.getMatchCards.bind(matchingAPI),
  getMatches: matchingAPI.getMatches.bind(matchingAPI),
  submitMatchAction: matchingAPI.submitMatchAction.bind(matchingAPI),
  swipeCard: matchingAPI.swipeCard.bind(matchingAPI),
  getMatchDetail: matchingAPI.getMatchDetail.bind(matchingAPI),
  getMatchList: matchingAPI.getMatchList.bind(matchingAPI),
  
  // 聊天相关方法
  getChatHistory: chatAPI.getChatHistory.bind(chatAPI),
  sendMessage: chatAPI.sendMessage.bind(chatAPI),
  markAsRead: chatAPI.markAsRead.bind(chatAPI),
  
  // 会员相关方法
  getMembershipInfo: membershipAPI.getMembershipInfo.bind(membershipAPI),
  createMembershipPayment: membershipAPI.createMembershipPayment.bind(membershipAPI),
  
  // 模拟数据方法（测试用）
  getMockMatchCards: matchingAPI.getMockMatchCards.bind(matchingAPI),
  clearTestMatches: matchingAPI.clearTestMatches.bind(matchingAPI),
  
  // API实例
  authAPI,
  userAPI,
  matchingAPI,
  chatAPI,
  membershipAPI
};