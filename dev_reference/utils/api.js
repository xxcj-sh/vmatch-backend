// 引入新创建的API模块
const apiModule = require('./api/index');

// 直接使用apiModule导出，避免重复绑定
module.exports = apiModule;