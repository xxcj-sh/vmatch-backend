// 匹配工具函数

/**
 * 清理所有本地匹配数据
 */
function clearAllMatches() {
  try {
    wx.removeStorageSync('testMatches');
    wx.setStorageSync('testMatches', []);
    console.log('所有匹配数据已清理');
    return true;
  } catch (error) {
    console.error('清理匹配数据失败:', error);
    return false;
  }
}

/**
 * 获取所有匹配数据
 */
function getAllMatches() {
  try {
    return wx.getStorageSync('testMatches') || [];
  } catch (error) {
    console.error('获取匹配数据失败:', error);
    return [];
  }
}

/**
 * 添加测试匹配数据
 */
function addTestMatches() {
  const testMatches = [
    {
      id: 'test_match_1',
      name: '张小明',
      avatar: '/images/icon-user.png',
      age: 28,
      location: '北京朝阳区',
      occupation: '产品经理',
      education: '硕士',
      height: 175,
      timestamp: new Date(Date.now() - 3600000).toISOString(), // 1小时前
      lastMessageTime: new Date(Date.now() - 3600000).toISOString(),
      reason: '你们都热爱旅行和美食！',
      isRead: false,
      unreadCount: 1,
      matchType: 'dating',
      card1: { name: '当前用户' },
      card2: { name: '张小明', age: 28 }
    },
    {
      id: 'test_match_2',
      name: '李美丽',
      avatar: '/images/icon-user.png',
      age: 25,
      location: '上海浦东新区',
      occupation: '设计师',
      education: '本科',
      height: 165,
      timestamp: new Date(Date.now() - 7200000).toISOString(), // 2小时前
      lastMessageTime: new Date(Date.now() - 7200000).toISOString(),
      reason: '兴趣相投，都喜欢摄影和阅读',
      isRead: true,
      unreadCount: 0,
      matchType: 'dating',
      card1: { name: '当前用户' },
      card2: { name: '李美丽', age: 25 }
    }
  ];

  try {
    wx.setStorageSync('testMatches', testMatches);
    console.log('测试匹配数据已添加');
    return true;
  } catch (error) {
    console.error('添加测试匹配数据失败:', error);
    return false;
  }
}

/**
 * 获取匹配数量
 */
function getMatchCount() {
  const matches = getAllMatches();
  return {
    total: matches.length,
    new: matches.filter(m => !m.isRead).length,
    contacted: matches.filter(m => m.isRead).length
  };
}

/**
 * 标记匹配为已读
 */
function markMatchAsRead(matchId) {
  try {
    const matches = getAllMatches();
    const matchIndex = matches.findIndex(m => m.id === matchId);
    
    if (matchIndex !== -1) {
      matches[matchIndex].isRead = true;
      matches[matchIndex].unreadCount = 0;
      wx.setStorageSync('testMatches', matches);
      return true;
    }
    return false;
  } catch (error) {
    console.error('标记匹配已读失败:', error);
    return false;
  }
}

// 导出函数
module.exports = {
  clearAllMatches,
  getAllMatches,
  addTestMatches,
  getMatchCount,
  markMatchAsRead
};