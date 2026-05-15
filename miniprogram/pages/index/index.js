// pages\index\index.js
const { BASE_URL } = require("../../utils/config");

Page({
  onShow() {
    const userId = wx.getStorageSync("user_id");

    if (userId) {
      wx.switchTab({
        url: "/pages/home/home"
      });
    } else {
      wx.redirectTo({
        url: "/pages/login/login"
      });
    }
  }
});