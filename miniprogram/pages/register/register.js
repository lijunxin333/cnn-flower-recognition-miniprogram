// pages/register/register.js
const { BASE_URL } = require("../../utils/config");

Page({
  data: {
    username: "",
    password: ""
  },

  onUsernameInput(e) {
    this.setData({
      username: e.detail.value
    });
  },

  onPasswordInput(e) {
    this.setData({
      password: e.detail.value
    });
  },

  handleRegister() {
    const { username, password } = this.data;

    if (!username || !password) {
      wx.showToast({
        title: "请输入完整信息",
        icon: "none"
      });
      return;
    }

    if (password.length < 6) {
      wx.showToast({
        title: "密码至少6位",
        icon: "none"
      });
      return;
    }

    wx.showLoading({ title: "注册中..." });

    wx.request({
      url: BASE_URL + "/user/register",
      method: "POST",
      data: {
        username,
        password
      },
    
      success: (res) => {
        wx.hideLoading();
    
        const data = res.data;
    
        // ❗统一用 code 判断
        if (data.code === 0) {
    
          wx.showToast({
            title: "注册成功",
            icon: "success"
          });
    
          setTimeout(() => {
            wx.navigateBack(); // 回登录页
          }, 500);
    
        } else {
          wx.showToast({
            title: data.msg || "注册失败",
            icon: "none"
          });
        }
      },
    
      fail: () => {
        wx.hideLoading();
        wx.showToast({
          title: "网络错误",
          icon: "none"
        });
      }
    });
  }
});