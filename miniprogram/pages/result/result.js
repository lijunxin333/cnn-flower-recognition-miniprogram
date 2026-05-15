// pages\result\result.js

const { BASE_URL } = require("../../utils/config");

Page({
  data: {
    result: {}
  },

  onLoad() {
    const eventChannel = this.getOpenerEventChannel();

    eventChannel.on("resultData", (res) => {
      const result = res.data;

      // ⭐ 置信度格式化
      result.top1.probText = (result.top1.prob * 100).toFixed(1);

      // ⭐ 用后端返回的 image（关键！）
      result.top1.img = BASE_URL + result.top1.image;

      // top3
      result.top3 = result.top3.map(item => ({
        ...item,
        probText: (item.prob * 100).toFixed(1)
      }));

      this.setData({ result });
    });
  },

  // 重新识别
  reChoose() {
    wx.navigateBack({ delta: 1 });
  },

  // ⭐ 收藏（改成后端版）
  saveResult() {
    const result = this.data.result;
    const userId = wx.getStorageSync("user_id");

    wx.request({
      url: BASE_URL + "/favorite/add",
      method: "POST",
      data: {
         user_id: userId,
        flower_id: result.top1.id
      },

      success: (res) => {
        if (res.data.msg === "exists") {
          wx.showToast({
            title: "已收藏",
            icon: "none"
          });
        } else {
          wx.showToast({
            title: "收藏成功",
            icon: "success"
          });
        }
      }
    });
  },
  goDetail() {
    const result = this.data.result;
  
    wx.navigateTo({
      url: "/pages/detail/detail",
      success: (res) => {
        res.eventChannel.emit("detailData", {
          id: result.top1.id,
          name: result.top1.name,
          img: result.top1.img
        });
      }
    });
  },
  // 从top3走
  goDetailFromTop3(e) {
    const item = e.currentTarget.dataset.item;
  
    wx.navigateTo({
      url: "/pages/detail/detail",
      success: (res) => {
        res.eventChannel.emit("detailData", {
          id: item.id,
          name: item.name
        });
      }
    });
  }
});