// pages\detail\detail.js
const { BASE_URL } = require("../../utils/config");

Page({
  data: {
    item: {},
    detail: {}
  },

  onLoad() {
    const eventChannel = this.getOpenerEventChannel();

    eventChannel.on("detailData", (data) => {

      // ⭐ 1. 先保存基础信息（收藏页传来的）
      this.setData({
        item: data
      });

      // ⭐ 2. 再去后端查完整详情
      wx.request({
        url: BASE_URL + "/flower/detail?id=" + data.id,
        success: (res) => {
      
          const d = res.data.data;
      
          this.setData({
            detail: {
              ...d,
              image_url: BASE_URL + d.image_path
            }
          });
      
          console.log("detail set:", this.data.detail);
        }
      });

    });
  }
});