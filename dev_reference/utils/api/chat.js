const ApiClient = require('./client');

class ChatAPI extends ApiClient {
  // 获取聊天记录
  async getChatHistory(matchId, page = 1, limit = 20) {
    if (wx.getStorageSync('testMode')) {
      console.log('测试模式：获取模拟聊天记录', matchId);
      
      // 生成一致的测试数据
      const mockMessages = [
        {
          id: 1,
          senderId: 'other',
          content: '你好，很高兴认识你！',
          timestamp: new Date(Date.now() - 3600000).toISOString(),
          type: 'text'
        },
        {
          id: 2,
          senderId: 'me',
          content: '你好，我也很高兴认识你！',
          timestamp: new Date(Date.now() - 3500000).toISOString(),
          type: 'text'
        },
        {
          id: 3,
          senderId: 'other',
          content: '你的个人资料看起来很不错',
          timestamp: new Date(Date.now() - 3400000).toISOString(),
          type: 'text'
        }
      ];
      
      return {
        list: mockMessages,
        total: mockMessages.length,
        page: 1,
        limit: 20
      };
    }

    try {
      const data = await this.request({
        url: `/chat/history/${matchId}`,
        method: 'GET',
        data: {
          page,
          limit
        }
      });
      
      return data;
    } catch (error) {
      console.error('获取聊天记录失败:', error);
      throw error;
    }
  }

  // 发送消息
  async sendMessage(matchId, content, type = 'text') {
    if (wx.getStorageSync('testMode')) {
      console.log('测试模式：发送模拟消息', { matchId, content });
      
      // 模拟发送成功
      return {
        id: Date.now(),
        senderId: 'me',
        content: content,
        timestamp: new Date().toISOString(),
        type: type
      };
    }

    try {
      const data = await this.request({
        url: '/chat/send',
        method: 'POST',
        data: {
          matchId,
          content,
          type
        }
      });
      
      return data;
    } catch (error) {
      console.error('发送消息失败:', error);
      throw error;
    }
  }

  // 标记消息已读
  async markAsRead(matchId) {
    if (wx.getStorageSync('testMode')) {
      console.log('测试模式：标记消息已读', matchId);
      
      // 更新本地存储的测试匹配记录
      const savedMatches = wx.getStorageSync('testMatches') || [];
      const updatedMatches = savedMatches.map(match => {
        if (match.id === parseInt(matchId)) {
          return { ...match, isRead: true };
        }
        return match;
      });
      
      wx.setStorageSync('testMatches', updatedMatches);
      return { success: true };
    }

    try {
      const data = await this.request({
        url: '/chat/read',
        method: 'POST',
        data: {
          matchId
        }
      });
      
      return data;
    } catch (error) {
      console.error('标记消息已读失败:', error);
      throw error;
    }
  }

  // 获取聊天消息（兼容旧方法名）
  async getChatMessages(matchId, page = 1, limit = 20) {
    return this.getChatHistory(matchId, page, limit);
  }
}

module.exports = ChatAPI;