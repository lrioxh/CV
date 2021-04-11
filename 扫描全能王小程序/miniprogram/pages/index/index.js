//index.js
const app = getApp()
// import html2canvas from 'html2canvas';
// require('./canvas2image.js');
// import Canvas2Image from 'canvas2image';

Page({
  data: {
    img:0,
    block_width:1,
    block_height:1,
    move_n:20,
    move_b:0.5,
    radius:101,
    sigma:32,
    radius_gray:101,
    sigma_gray:32,
    usm_k:0.3,
    usm_k_gray:0.3
  },

  onLoad: function() {
  },
  

  // 上传图片
  doUpload: function () {

    var that = this;
    // 选择图片
    wx.chooseImage({
      count: 1,
      sizeType: ['compressed'],
      sourceType: ['album', 'camera'],
      success: function (res) {
        wx.getImageInfo({
          src: res.tempFilePaths[0],
          success: (imgInfo) => {
            let {
              width,
              height,
              imgPath
            } = imgInfo;
            var path = res.tempFilePaths[0]
            wx.createSelectorQuery()
              .select('#canvas')
              .fields({
                node: true,
                size: true,
              })
              .exec((res) => {
                const canvas = res[0].node
                console.log(res[0])
                const ctx = canvas.getContext('2d')

                const img = canvas.createImage()
                img.onload = () => {
                  var scale = 1.0
                  var sw = img.width * scale
                  var sh = img.height* scale

                  var pixelRatio = 0
                  wx.getSystemInfo({
                    success: function (res) {
                      pixelRatio = res.pixelRatio
                    },
                    fail: function () {
                      pixelRatio = 0
                    }
                  })
                  ctx.scale(pixelRatio, pixelRatio)
                  canvas.width = img.width
                  canvas.height = img.height
                  var w = canvas.width;
                  var h = canvas.height;
                  ctx.clearRect(0, 0, img.width, img.height)
                  
                  ctx.drawImage(img, -sw / 2 + w / 2, -sh / 2 + h / 2, img.width, img.height)
                  ctx.fillStyle = 'white';
                  ctx.fill();
                  var imgData = ctx.getImageData(0, 0, width, height);
                  console.log(imgData)

                  var pixels = imgData.data;
                  var pixelCount = width * height;
                  var pixelArray = [];
                  // 对像素数据进行预处理
                }
                img.src = path
              })
          }
        })

        var tempFilePaths = res.tempFilePaths;
        that.setData({
          img: tempFilePaths[0],
          original: tempFilePaths[0]
        });
        console.log('ok!');
      },
      fail: e => {
        console.error(e)
      }
    })
  },
  previewImg: function () {
    //获取当前图片的下标
    //所有图片
    var img = this.data.img;
    wx.previewImage({
      //当前显示图片
      current: img,
      //所有图片
      urls: []
    })
  },

  deleteImage:function(){
    var that = this;
    that.setData({
      img: 0,
      original:0
    });
  },

  saveImg: function () {
    var that = this;
    wx.saveImageToPhotosAlbum({
      //shareImgSrc为canvas赋值的图片路径
      filePath: that.data.img,
      success(res) {
        console.log(res);
        wx.showModal({
          title: '保存成功',
          content: '图片成功保存到相册了~',
          showCancel: false,
          confirmText: '确认',
          confirmColor: '#21e6c1',
          success: function (res) {
            if (res.confirm) {
              console.log('用户点击确定');
            }
          }
        })
      },
      fail(res){
        console.log(res)
      }
    })
  },

  resetImg:function(){
    var that = this;
    that.setData({
      img:that.data.original
    })
    wx.getImageInfo({
      src: that.data.img,
      success: (imgInfo) => {
        let {
          width,
          height,
          imgPath
        } = imgInfo;
        var path = that.data.img
        wx.createSelectorQuery()
          .select('#canvas')
          .fields({
            node: true,
            size: true,
          })
          .exec((res) => {
            const canvas = res[0].node
            console.log(res[0])
            const ctx = canvas.getContext('2d')

            const img = canvas.createImage()
            img.onload = () => {
              var scale = 1.0
              var sw = img.width * scale
              var sh = img.height * scale

              var pixelRatio = 0
              wx.getSystemInfo({
                success: function (res) {
                  pixelRatio = res.pixelRatio
                },
                fail: function () {
                  pixelRatio = 0
                }
              })
              ctx.scale(pixelRatio, pixelRatio)
              canvas.width = img.width
              canvas.height = img.height
              var w = canvas.width;
              var h = canvas.height;
              ctx.clearRect(0, 0, img.width, img.height)

              ctx.drawImage(img, -sw / 2 + w / 2, -sh / 2 + h / 2, img.width, img.height)
              ctx.fillStyle = 'white';
              ctx.fill();
            }
            img.src = path
          })
      }
    })
  },
  otsuSeperate:function(){
    function otsu(imgData){
      var non_zero = imgData.filter((item) => { return item > 0});
      var max_sigma = 0
      var th = 0
      var g_group = []
      var max_sigma_counts = 1
      var i = 0
      var gray_counts_groups = new Array(256)
      
      for(i=0;i<256;i++){
        gray_counts_groups[i] = 0
      }
      var left_color = 0
      var right_color = 0
      for(i=0;i<non_zero.length;i++){
        gray_counts_groups[non_zero[i]] += 1
        right_color += non_zero[i]
      }
      var left = 0
      var right = non_zero.length

      for(i=0;i<=256;i++){
        left += gray_counts_groups[i]
        right -= gray_counts_groups[i]

        if(left>0 && right>0){
          left_color += gray_counts_groups[i] * i
          right_color -= gray_counts_groups[i] * i
          var mean1 = left_color / left
          var mean2 = right_color / right
          var p1 = left/ non_zero.length
          var sigma = p1 * (1 - p1) * (mean1 - mean2) ** 2
          // g_group.push(sigma)
          if (max_sigma < sigma) {
            max_sigma = sigma
            th = i
            max_sigma_counts = 1
          } else if (max_sigma == sigma) {
            max_sigma_counts += 1
          }
        }
      }

      // th = parseInt(th + (g_group.filter((item) => { return item == max_sigma}).length)*0.5)
      th = parseInt(th+max_sigma_counts*0.5)
      return th

    }

    // 正式执行
    var that = this;
    wx.getImageInfo({
      src: that.data.img,
      success: (imgInfo) => {
        let {
          width,
          height,
          imgPath
        } = imgInfo;
        var path = that.data.img
        wx.createSelectorQuery()
          .select('#canvas')
          .fields({
            node: true,
            size: true,
          })
          .exec((res) => {
            const canvas = res[0].node
            console.log(res[0])
            const ctx = canvas.getContext('2d')

            const img = canvas.createImage()
            img.onload = () => {
              var scale = 1.0
              var sw = img.width * scale
              var sh = img.height * scale

              var pixelRatio = 0
              wx.getSystemInfo({
                success: function (res) {
                  pixelRatio = res.pixelRatio
                },
                fail: function () {
                  pixelRatio = 0
                }
              })
              ctx.scale(pixelRatio, pixelRatio)
              canvas.width = img.width
              canvas.height = img.height
              var w = canvas.width;
              var h = canvas.height;
              ctx.clearRect(0, 0, img.width, img.height)

              ctx.drawImage(img, -sw / 2 + w / 2, -sh / 2 + h / 2, img.width, img.height)
              ctx.fillStyle = 'white';
              ctx.fill();
              var imgData = ctx.getImageData(0, 0, width, height);
              // 变成灰度
              for (var i = 0; i < imgData.data.length; i += 4) {
                var gray = parseInt((imgData.data[i + 0] + imgData.data[i + 1] + imgData.data[i + 2]) / 3)
                imgData.data[i + 0] = gray;
                imgData.data[i + 1] = gray;
                imgData.data[i + 2] = gray;
                imgData.data[i + 3] = 255;
              }

              var newImgData = ctx.createImageData(width, height);
              var block = [that.data.block_height, that.data.block_width]
              var unit_height = parseInt(height/ block[0])
              var unit_width = parseInt(width / block[1])
              // var new_img_data = []
              
              var blocks = []; //多个块
              for (var i = 0; i < block[0] * block[1]; i++) {
                blocks.push([])
              }
              var th_groups = []; //阈值组

              var counts = 0
              for (var i = 0; i < imgData.data.length; i = i + 4) {

                var index_height = parseInt(counts / width)
                var index_width = counts % width
                var index_x_block = parseInt(index_height / unit_height)
                var index_y_block = parseInt(index_width / unit_width)
                if (index_x_block >= block[0]) {
                  index_x_block = block[0] - 1
                }
                if (index_y_block >= block[1]) {
                  index_y_block = block[1] - 1
                }
                var block_index = index_x_block * block[1] + index_y_block
                blocks[block_index].push(imgData.data[i])
                counts += 1
              }
              // console.log(blocks)
              for (var i = 0; i < blocks.length; i++) {
                var th = otsu(blocks[i])
                th_groups.push(th)
              }
              // console.log(th_groups)

              counts = 0
              for (var i = 0; i < newImgData.data.length; i = i + 4) {

                var index_height = parseInt(counts / width)
                var index_width = counts % width
                var index_x_block = parseInt(index_height / unit_height)
                var index_y_block = parseInt(index_width / unit_width)
                if (index_x_block >= block[0]) {
                  index_x_block = block[0] - 1
                }
                if (index_y_block >= block[1]) {
                  index_y_block = block[1] - 1
                }
                var block_index = index_x_block * block[1] + index_y_block
                if (imgData.data[i] > th_groups[block_index]) {
                  newImgData.data[i] = 255
                  newImgData.data[i + 1] = 255
                  newImgData.data[i + 2] = 255
                  newImgData.data[i+3] = 255
                } else {
                  newImgData.data[i] = 0
                  newImgData.data[i + 1] = 0
                  newImgData.data[i + 2] = 0
                  newImgData.data[i + 3] = 255
                }
                counts += 1
              }
              // console.log(newImgData.data)
              ctx.putImageData(newImgData, 0, 0);
            }
            img.src = path
          })
      }
    })

  },
  moveThreshold:function(){
    var that = this;
    wx.getImageInfo({
      src: that.data.img,
      success: (imgInfo) => {
        let {
          width,
          height,
          imgPath
        } = imgInfo;
        var path = that.data.img
        wx.createSelectorQuery()
          .select('#canvas')
          .fields({
            node: true,
            size: true,
          })
          .exec((res) => {
            const canvas = res[0].node
            console.log(res[0])
            const ctx = canvas.getContext('2d')

            const img = canvas.createImage()
            img.onload = () => {
              var scale = 1.0
              var sw = img.width * scale
              var sh = img.height * scale

              var pixelRatio = 0
              wx.getSystemInfo({
                success: function (res) {
                  pixelRatio = res.pixelRatio
                },
                fail: function () {
                  pixelRatio = 0
                }
              })
              ctx.scale(pixelRatio, pixelRatio)
              canvas.width = img.width
              canvas.height = img.height
              var w = canvas.width;
              var h = canvas.height;
              ctx.clearRect(0, 0, img.width, img.height)

              ctx.drawImage(img, -sw / 2 + w / 2, -sh / 2 + h / 2, img.width, img.height)
              ctx.fillStyle = 'white';
              ctx.fill();
              var imgData = ctx.getImageData(0, 0, width, height);
              // 变成灰度
              for (var i = 0; i < imgData.data.length; i += 4) {
                var gray = parseInt((imgData.data[i + 0] + imgData.data[i + 1] + imgData.data[i + 2]) / 3)
                imgData.data[i + 0] = gray;
                imgData.data[i + 1] = gray;
                imgData.data[i + 2] = gray;
                imgData.data[i + 3] = 255;
              }
              var newImgData = ctx.createImageData(width, height);

              var temp = new Array(width*height)
              var counts = 0
              for (var i = 0; i < imgData.data.length; i = i + 4) {

                var index_height = parseInt(counts / width)
                var index_width = counts % width
                if(index_height%2 == 0){
                  temp[index_height*width+index_width] = imgData.data[i]
                }else{
                  temp[index_height * width + index_width] = imgData.data[4*(index_height*width+width-1-index_width)]
                }
                counts += 1
              }
              var m_pre = 0
              var counts = 0
              var n =that.data.move_n
              var b = that.data.move_b
              for (var i = 0; i < imgData.data.length; i = i + 4) {
                var index_height = parseInt(counts / width)
                var index_width = counts % width
                var dif = 0
                if(counts<n){
                  dif = temp[counts]
                }else{
                  dif = temp[counts] - temp[counts - n]
                }
                dif *= 1/n
                var m_now = m_pre + dif
                m_pre = m_now
                if(imgData.data[i]>b*m_now){
                  newImgData.data[i] = 255
                  newImgData.data[i + 1] = 255
                  newImgData.data[i + 2] = 255
                  newImgData.data[i + 3] = 255
                }else{
                  newImgData.data[i] = 0
                  newImgData.data[i + 1] = 0
                  newImgData.data[i + 2] = 0
                  newImgData.data[i + 3] = 255
                }
                counts +=1
              }
              ctx.putImageData(newImgData, 0, 0);
            }
            img.src = path
          })
      }
    })

  },
  linearTransform:function(){
    var linear_table = [0,0   ,0   ,0   ,1   ,1  , 1   ,1  , 2  , 2  , 2  , 2  , 3  , 3  , 3  , 3 , 4  , 4,
   4 ,  4  , 5   ,5 ,  5  , 5 ,  6  , 6  , 6 , 6   ,7   ,7  , 7  , 7 ,  8  , 8  , 8 ,  8,
   9 ,  9 ,  9  , 9  ,10 , 10 , 10 , 10,  11,  11 , 11 , 11,  12 , 12 , 12 , 12 , 13,  13,
  13,  13,  14 , 14 , 14 , 14 , 15 , 15 , 15 , 15,  16 , 17 , 19  ,21  ,23 , 24 , 26,  28,
  30 , 31,  33,  35,  37,  38 , 40 , 42 , 44 , 45 , 47  ,49,  51,  52,  54 , 56,  58 , 59,
  61,  63 , 65 , 66 , 68 , 70,  72 , 73 , 75 , 77 , 79,  80,  82 , 84 , 86 , 87, 89  ,91,
  93,  94 , 96 , 98 ,100 ,101 ,103, 105, 107 ,108, 110 ,112 ,114, 115 ,117 ,119, 121, 122,
 124, 126 ,128, 129, 131, 132 ,134, 135, 137 ,138 ,140, 142 ,143 ,145 ,146, 148 ,149 ,151,
 152, 154 ,156, 157, 159, 160, 162 ,163 ,165, 166 ,168 ,170 ,171, 173 ,174 ,176, 177 ,179,
 180, 182, 184, 185, 187 ,188, 190, 191 ,193, 194, 196 ,198 ,199 ,201, 202 ,204 ,205 ,207,
 208, 210, 212, 213 ,215 ,216, 218, 219 ,221 ,222 ,224, 226 ,227 ,229, 230, 232 ,233 ,235,
 236, 238, 240, 240, 240 ,240, 241, 241, 241, 241, 242, 242 ,242, 243, 243 ,243 ,243 ,244,
 244 ,244 ,244 ,245, 245, 245, 246, 246 ,246 ,246, 247 ,247, 247 ,247 ,248 ,248 ,248, 249,
 249 ,249, 249, 250 ,250, 250, 250 ,251 ,251 ,251,252, 252, 252 ,252 ,253, 253, 253, 253,
 254 ,254 ,254 ,255];
    var that = this;
    wx.getImageInfo({
      src: that.data.img,
      success: (imgInfo) => {
        let {
          width,
          height,
          imgPath
        } = imgInfo;
        var path = that.data.img
        wx.createSelectorQuery()
          .select('#canvas')
          .fields({
            node: true,
            size: true,
          })
          .exec((res) => {
            const canvas = res[0].node
            console.log(res[0])
            const ctx = canvas.getContext('2d')

            const img = canvas.createImage()
            img.onload = () => {
              var scale = 1.0
              var sw = img.width * scale
              var sh = img.height * scale

              var pixelRatio = 0
              wx.getSystemInfo({
                success: function (res) {
                  pixelRatio = res.pixelRatio
                },
                fail: function () {
                  pixelRatio = 0
                }
              })
              ctx.scale(pixelRatio, pixelRatio)
              canvas.width = img.width
              canvas.height = img.height
              var w = canvas.width;
              var h = canvas.height;
              ctx.clearRect(0, 0, img.width, img.height)

              ctx.drawImage(img, -sw / 2 + w / 2, -sh / 2 + h / 2, img.width, img.height)
              ctx.fillStyle = 'white';
              ctx.fill();
              var imgData = ctx.getImageData(0, 0, width, height);
              var newImgData = ctx.createImageData(width, height);

              for(var i=0;i<imgData.data.length;i=i+4){
                newImgData.data[i] = linear_table[imgData.data[i]]
                newImgData.data[i+1] = linear_table[imgData.data[i+1]]
                newImgData.data[i+2] = linear_table[imgData.data[i+2]]
                newImgData.data[i+3] = 255
              }

              ctx.putImageData(newImgData, 0, 0);
            }
            img.src = path
          })
      }
    })
  },
  histEqual:function(){
    var that = this;
    wx.getImageInfo({
      src: that.data.img,
      success: (imgInfo) => {
        let {
          width,
          height,
          imgPath
        } = imgInfo;
        var path = that.data.img
        wx.createSelectorQuery()
          .select('#canvas')
          .fields({
            node: true,
            size: true,
          })
          .exec((res) => {
            const canvas = res[0].node
            console.log(res[0])
            const ctx = canvas.getContext('2d')

            const img = canvas.createImage()
            img.onload = () => {
              var scale = 1.0
              var sw = img.width * scale
              var sh = img.height * scale

              var pixelRatio = 0
              wx.getSystemInfo({
                success: function (res) {
                  pixelRatio = res.pixelRatio
                },
                fail: function () {
                  pixelRatio = 0
                }
              })
              ctx.scale(pixelRatio, pixelRatio)
              canvas.width = img.width
              canvas.height = img.height
              var w = canvas.width;
              var h = canvas.height;
              ctx.clearRect(0, 0, img.width, img.height)

              ctx.drawImage(img, -sw / 2 + w / 2, -sh / 2 + h / 2, img.width, img.height)
              ctx.fillStyle = 'white';
              ctx.fill();
              var imgData = ctx.getImageData(0, 0, width, height);
              var newImgData = ctx.createImageData(width, height);

              var hist_val = new Array(3*256)
              for(var i=0;i<3*256;i++){
                hist_val[i] = 0
              }
              for(var i=0;i<imgData.data.length;i=i+4){
                // 存储格式，前256为R，中为G，后为B
                hist_val[imgData.data[i]] += 1/(width*height)
                hist_val[256 + imgData.data[i + 1]] += 1 / (width * height)
                hist_val[256 * 2 + imgData.data[i + 2]] += 1 / (width * height)
              }
              var hist_cdf = hist_val
              for(var i=1;i<256;i++){
                hist_cdf[i] = hist_cdf[i] + hist_cdf[i-1]
                hist_cdf[256 + i] = hist_cdf[256 + i] + hist_cdf[256 +i - 1]
                hist_cdf[256 * 2 + i] = hist_cdf[256 * 2 + i] + hist_cdf[256 * 2 +i - 1]
                hist_cdf[i - 1] = parseInt(255*hist_cdf[i - 1]+0.1)
                hist_cdf[256 + i - 1] = parseInt(255 * hist_cdf[256 + i - 1] + 0.1)
                hist_cdf[256 * 2 + i - 1] = parseInt(255 * hist_cdf[256 * 2 +i - 1] + 0.1)
              }
              hist_cdf[255] = parseInt(255*hist_cdf[255]+0.1)
              hist_cdf[255+256] = parseInt(255 * hist_cdf[255+256] + 0.1)
              hist_cdf[255+256*2] = parseInt(255 * hist_cdf[255+256*2] + 0.1)
              for(var i=0;i<newImgData.data.length;i=i+4){
                newImgData.data[i] = hist_cdf[imgData.data[i]]
                newImgData.data[i + 1] = hist_cdf[256 + imgData.data[i+1]]
                newImgData.data[i + 2] = hist_cdf[256*2 + imgData.data[i + 2]]
                newImgData.data[i+3] = 255
              }

              ctx.putImageData(newImgData, 0, 0);
            }
            img.src = path
          })
      }
    })
  },
  sharpen:function(){
    var that = this;
    wx.getImageInfo({
      src: that.data.img,
      success: (imgInfo) => {
        let {
          width,
          height,
          imgPath
        } = imgInfo;
        var path = that.data.img
        wx.createSelectorQuery()
          .select('#canvas')
          .fields({
            node: true,
            size: true,
          })
          .exec((res) => {
            const canvas = res[0].node
            console.log(res[0])
            const ctx = canvas.getContext('2d')

            const img = canvas.createImage()
            img.onload = () => {
              var scale = 1.0
              var sw = img.width * scale
              var sh = img.height * scale

              var pixelRatio = 0
              wx.getSystemInfo({
                success: function (res) {
                  pixelRatio = res.pixelRatio
                },
                fail: function () {
                  pixelRatio = 0
                }
              })
              ctx.scale(pixelRatio, pixelRatio)
              canvas.width = img.width
              canvas.height = img.height
              var w = canvas.width;
              var h = canvas.height;
              ctx.clearRect(0, 0, img.width, img.height)

              ctx.drawImage(img, -sw / 2 + w / 2, -sh / 2 + h / 2, img.width, img.height)
              ctx.fillStyle = 'white';
              ctx.fill();
              var imgData = ctx.getImageData(0, 0, width, height);
              var newImgData = ctx.createImageData(width, height);

              var kernel = [0,-1,0,-1,5,-1,0,-1,0] //参数
              var ksize = parseInt(Math.sqrt(kernel.length))
              var border = parseInt(ksize/2)
              var counts = 0
              var skip_counts = 0
              for (var i = 0; i < imgData.data.length; i = i + 4) {

                var index_height = parseInt(counts / width)
                var index_width = counts % width
                if(index_height<border || index_height>=height-border || index_width<border || index_width>=width - border){
                  newImgData.data[i] = imgData.data[i]
                  newImgData.data[i + 1] = imgData.data[i+1]
                  newImgData.data[i + 2] = imgData.data[i+2]
                  newImgData.data[i + 3] = 255
                  skip_counts += 1
                  counts += 1
                  continue
                }
                var sum = [0,0,0]
                for(var j =0;j<kernel.length;j++){
                  var index_kernal_x = parseInt(j/ksize)
                  var index_kernal_y = j%ksize - (ksize-1)/2
                  sum[0] += kernel[j]*imgData.data[i+index_kernal_x*4*width+4*index_kernal_y]
                  sum[1] += kernel[j] * imgData.data[i+1 + index_kernal_x * 4 * width + 4 * index_kernal_y]
                  sum[2] += kernel[j] * imgData.data[i + 2 + index_kernal_x * 4 * width + 4 * index_kernal_y]
                }
                newImgData.data[i] = sum[0]
                newImgData.data[i+1] = sum[1]
                newImgData.data[i+2] = sum[2]
                newImgData.data[i+3] = 255
                
                counts += 1
              }
              console.log(skip_counts)

              ctx.putImageData(newImgData, 0, 0);
            }
            img.src = path
          })
      }
    })
  },
  usm:function(){
    function gaussBlur1(imgData, ctx, radius, sigma) {
      var pixes = imgData.data;
      var width = imgData.width;
      var height = imgData.height;
      var newImgData = ctx.createImageData(width, height);
      var gaussMatrix = [],
        gaussSum = 0,
        x, y,
        r, g, b, a,
        i, j, k, len;


      radius = Math.floor(radius) || 3;
      sigma = sigma || radius / 3;

      a = 1 / (Math.sqrt(2 * Math.PI) * sigma);
      b = -1 / (2 * sigma * sigma);
      //生成高斯矩阵
      for (i = 0, x = -radius; x <= radius; x++ , i++) {
        g = a * Math.exp(b * x * x);
        gaussMatrix[i] = g;
        gaussSum += g;

      }
      //归一化, 保证高斯矩阵的值在[0,1]之间
      for (i = 0, len = gaussMatrix.length; i < len; i++) {
        gaussMatrix[i] /= gaussSum;
      }
      //x 方向一维高斯运算
      for (y = 0; y < height; y++) {
        for (x = 0; x < width; x++) {
          r = g = b = a = 0;
          gaussSum = 0;
          for (j = -radius; j <= radius; j++) {
            k = x + j;
            if (k >= 0 && k < width) {//确保 k 没超出 x 的范围
              //r,g,b,a 四个一组
              i = (y * width + k) * 4;
              r += pixes[i] * gaussMatrix[j + radius];
              g += pixes[i + 1] * gaussMatrix[j + radius];
              b += pixes[i + 2] * gaussMatrix[j + radius];
              // a += pixes[i + 3] * gaussMatrix[j];
              gaussSum += gaussMatrix[j + radius];
            }
          }
          i = (y * width + x) * 4;
          // 除以 gaussSum 是为了消除处于边缘的像素, 高斯运算不足的问题
          newImgData.data[i] = r / gaussSum
          newImgData.data[i + 1] = g / gaussSum;
          newImgData.data[i + 2] = b / gaussSum;
          newImgData.data[i + 3] = 255

        }
      }
      //y 方向一维高斯运算
      for (x = 0; x < width; x++) {
        for (y = 0; y < height; y++) {
          r = g = b = a = 0;
          gaussSum = 0;
          for (j = -radius; j <= radius; j++) {
            k = y + j;
            if (k >= 0 && k < height) {//确保 k 没超出 y 的范围
              i = (k * width + x) * 4;
              r += newImgData.data[i] * gaussMatrix[j + radius];
              g += newImgData.data[i + 1] * gaussMatrix[j + radius];
              b += newImgData.data[i + 2] * gaussMatrix[j + radius];
              // a += pixes[i + 3] * gaussMatrix[j];
              gaussSum += gaussMatrix[j + radius];
            }
          }
          i = (y * width + x) * 4;
          newImgData.data[i] = r / gaussSum
          newImgData.data[i + 1] = g / gaussSum;
          newImgData.data[i + 2] = b / gaussSum;
          newImgData.data[i + 3] = 255
        }
      }
      //end
      return newImgData;
    }

    // 正式运行
    var that = this;
    wx.getImageInfo({
      src: that.data.img,
      success: (imgInfo) => {
        let {
          width,
          height,
          imgPath
        } = imgInfo;
        var path = that.data.img
        wx.createSelectorQuery()
          .select('#canvas')
          .fields({
            node: true,
            size: true,
          })
          .exec((res) => {
            const canvas = res[0].node
            console.log(res[0])
            const ctx = canvas.getContext('2d')

            const img = canvas.createImage()
            img.onload = () => {
              var scale = 1.0
              var sw = img.width * scale
              var sh = img.height * scale

              var pixelRatio = 0
              wx.getSystemInfo({
                success: function (res) {
                  pixelRatio = res.pixelRatio
                },
                fail: function () {
                  pixelRatio = 0
                }
              })
              ctx.scale(pixelRatio, pixelRatio)
              canvas.width = img.width
              canvas.height = img.height
              var w = canvas.width;
              var h = canvas.height;
              ctx.clearRect(0, 0, img.width, img.height)

              ctx.drawImage(img, -sw / 2 + w / 2, -sh / 2 + h / 2, img.width, img.height)
              ctx.fillStyle = 'white';
              ctx.fill();
              var k = that.data.usm_k
              var radius = that.data.radius
              var sigma = that.data.sigma
              var imgData = ctx.getImageData(0, 0, width, height);
              var newImgData = gaussBlur1(imgData, ctx, radius, sigma)
              for(var i=0;i<imgData.data.length;i=i+4){
                newImgData.data[i] = parseInt((1 + k) * imgData.data[i] - k * newImgData.data[i])
                newImgData.data[i+1] = parseInt((1 + k) * imgData.data[i+1] - k * newImgData.data[i+1])
                newImgData.data[i+2] = parseInt((1 + k) * imgData.data[i+2] - k * newImgData.data[i+2])
              }

              ctx.putImageData(newImgData, 0, 0);
              console.log("convert ok!")
            }
            img.src = path
          })
      }
    })
  },
  gaussianFilter:function(){
    function gaussBlur1(imgData,ctx, radius, sigma) {
      var pixes = imgData.data;
      var width = imgData.width;
      var height = imgData.height;
      var newImgData = ctx.createImageData(width, height);
      var gaussMatrix = [],
        gaussSum = 0,
        x, y,
        r, g, b, a,
        i, j, k, len;


      radius = Math.floor(radius) || 3;
      sigma = sigma || radius / 3;

      a = 1 / (Math.sqrt(2 * Math.PI) * sigma);
      b = -1 / (2 * sigma * sigma);
      //生成高斯矩阵
      for (i = 0, x = -radius; x <= radius; x++ , i++) {
        g = a * Math.exp(b * x * x);
        gaussMatrix[i] = g;
        gaussSum += g;

      }
      //归一化, 保证高斯矩阵的值在[0,1]之间
      for (i = 0, len = gaussMatrix.length; i < len; i++) {
        gaussMatrix[i] /= gaussSum;
      }
      //x 方向一维高斯运算
      for (y = 0; y < height; y++) {
        for (x = 0; x < width; x++) {
          r = g = b = a = 0;
          gaussSum = 0;
          for (j = -radius; j <= radius; j++) {
            k = x + j;
            if (k >= 0 && k < width) {//确保 k 没超出 x 的范围
              //r,g,b,a 四个一组
              i = (y * width + k) * 4;
              r += pixes[i] * gaussMatrix[j + radius];
              g += pixes[i + 1] * gaussMatrix[j + radius];
              b += pixes[i + 2] * gaussMatrix[j + radius];
              // a += pixes[i + 3] * gaussMatrix[j];
              gaussSum += gaussMatrix[j + radius];
            }
          }
          i = (y * width + x) * 4;
          // 除以 gaussSum 是为了消除处于边缘的像素, 高斯运算不足的问题
          // console.log(gaussSum)
          pixes[i] = r / gaussSum;
          pixes[i + 1] = g / gaussSum;
          pixes[i + 2] = b / gaussSum;
          newImgData.data[i] = pixes[i]
          newImgData.data[i+1] = pixes[i+1]
          newImgData.data[i + 2] = pixes[i + 2]
          newImgData.data[i+3]=255

          // pixes[i + 3] = a ;
        }
      }
      //y 方向一维高斯运算
      for (x = 0; x < width; x++) {
        for (y = 0; y < height; y++) {
          r = g = b = a = 0;
          gaussSum = 0;
          for (j = -radius; j <= radius; j++) {
            k = y + j;
            if (k >= 0 && k < height) {//确保 k 没超出 y 的范围
              i = (k * width + x) * 4;
              r += pixes[i] * gaussMatrix[j + radius];
              g += pixes[i + 1] * gaussMatrix[j + radius];
              b += pixes[i + 2] * gaussMatrix[j + radius];
              // a += pixes[i + 3] * gaussMatrix[j];
              gaussSum += gaussMatrix[j + radius];
            }
          }
          i = (y * width + x) * 4;
          pixes[i] = r / gaussSum;
          pixes[i + 1] = g / gaussSum;
          pixes[i + 2] = b / gaussSum;
          newImgData.data[i] = pixes[i]
          newImgData.data[i + 1] = pixes[i + 1]
          newImgData.data[i + 2] = pixes[i + 2]
          newImgData.data[i + 3] = 255
          // pixes[i] = r ;
          // pixes[i + 1] = g ;
          // pixes[i + 2] = b ;
          // pixes[i + 3] = a ;
        }
      }
      //end
      // newImgData.data = pixes;
      return newImgData;
    }

    // 正式运行
    var that = this;
    wx.getImageInfo({
      src: that.data.img,
      success: (imgInfo) => {
        let {
          width,
          height,
          imgPath
        } = imgInfo;
        var path = that.data.img
        wx.createSelectorQuery()
          .select('#canvas')
          .fields({
            node: true,
            size: true,
          })
          .exec((res) => {
            const canvas = res[0].node
            console.log(res[0])
            const ctx = canvas.getContext('2d')

            const img = canvas.createImage()
            img.onload = () => {
              var scale = 1.0
              var sw = img.width * scale
              var sh = img.height * scale

              var pixelRatio = 0
              wx.getSystemInfo({
                success: function (res) {
                  pixelRatio = res.pixelRatio
                },
                fail: function () {
                  pixelRatio = 0
                }
              })
              ctx.scale(pixelRatio, pixelRatio)
              canvas.width = img.width
              canvas.height = img.height
              var w = canvas.width;
              var h = canvas.height;
              ctx.clearRect(0, 0, img.width, img.height)

              ctx.drawImage(img, -sw / 2 + w / 2, -sh / 2 + h / 2, img.width, img.height)
              ctx.fillStyle = 'white';
              ctx.fill();
              var imgData = ctx.getImageData(0, 0, width, height);
              // var newImgData = ctx.createImageData(width, height);
              var radius = that.data.radius
              var sigma = that.data.sigma
              var newImgData = gaussBlur1(imgData,ctx,radius,sigma)

              ctx.putImageData(newImgData, 0, 0);
              console.log("convert ok!")
            }
            img.src = path
          })
      }
    })

  },
  removeShadow:function(){
    function gaussBlur1(imgData, ctx, radius, sigma) {
      var pixes = imgData.data;
      var width = imgData.width;
      var height = imgData.height;
      var newImgData = ctx.createImageData(width, height);
      var gaussMatrix = [],
        gaussSum = 0,
        x, y,
        r, g, b, a,
        i, j, k, len;
      radius = Math.floor(radius) || 3;
      sigma = sigma || radius / 3;

      a = 1 / (Math.sqrt(2 * Math.PI) * sigma);
      b = -1 / (2 * sigma * sigma);
      //生成高斯矩阵
      for (i = 0, x = -radius; x <= radius; x++ , i++) {
        g = a * Math.exp(b * x * x);
        gaussMatrix[i] = g;
        gaussSum += g;

      }
      //归一化, 保证高斯矩阵的值在[0,1]之间
      for (i = 0, len = gaussMatrix.length; i < len; i++) {
        gaussMatrix[i] /= gaussSum;
      }
      //x 方向一维高斯运算
      for (y = 0; y < height; y++) {
        for (x = 0; x < width; x++) {
          r = g = b = a = 0;
          gaussSum = 0;
          for (j = -radius; j <= radius; j++) {
            k = x + j;
            if (k >= 0 && k < width) {//确保 k 没超出 x 的范围
              //r,g,b,a 四个一组
              i = (y * width + k) * 4;
              r += pixes[i] * gaussMatrix[j + radius];
              g += pixes[i + 1] * gaussMatrix[j + radius];
              b += pixes[i + 2] * gaussMatrix[j + radius];
              // a += pixes[i + 3] * gaussMatrix[j];
              gaussSum += gaussMatrix[j + radius];
            }
          }
          i = (y * width + x) * 4;
          // 除以 gaussSum 是为了消除处于边缘的像素, 高斯运算不足的问题
          newImgData.data[i] = r / gaussSum
          newImgData.data[i + 1] = g / gaussSum;
          newImgData.data[i + 2] = b / gaussSum;
          newImgData.data[i + 3] = 255

          // pixes[i + 3] = a ;
        }
      }
      //y 方向一维高斯运算
      for (x = 0; x < width; x++) {
        for (y = 0; y < height; y++) {
          r = g = b = a = 0;
          gaussSum = 0;
          for (j = -radius; j <= radius; j++) {
            k = y + j;
            if (k >= 0 && k < height) {//确保 k 没超出 y 的范围
              i = (k * width + x) * 4;
              r += newImgData.data[i] * gaussMatrix[j + radius];
              g += newImgData.data[i+1]* gaussMatrix[j + radius];
              b += newImgData.data[i+2] * gaussMatrix[j + radius];
              gaussSum += gaussMatrix[j + radius];
            }
          }
          i = (y * width + x) * 4;
          newImgData.data[i] = r / gaussSum
          newImgData.data[i + 1] = g / gaussSum;
          newImgData.data[i + 2] = b / gaussSum;
          newImgData.data[i + 3] = 255
        }
      }
      return newImgData;
    }

    // 正式运行
    var that = this;
    wx.getImageInfo({
      src: that.data.img,
      success: (imgInfo) => {
        let {
          width,
          height,
          imgPath
        } = imgInfo;
        var path = that.data.img
        wx.createSelectorQuery()
          .select('#canvas')
          .fields({
            node: true,
            size: true,
          })
          .exec((res) => {
            const canvas = res[0].node
            console.log(res[0])
            const ctx = canvas.getContext('2d')

            const img = canvas.createImage()
            img.onload = () => {
              var scale = 1.0
              var sw = img.width * scale
              var sh = img.height * scale

              var pixelRatio = 0
              wx.getSystemInfo({
                success: function (res) {
                  pixelRatio = res.pixelRatio
                },
                fail: function () {
                  pixelRatio = 0
                }
              })
              ctx.scale(pixelRatio, pixelRatio)
              canvas.width = img.width
              canvas.height = img.height
              var w = canvas.width;
              var h = canvas.height;
              ctx.clearRect(0, 0, img.width, img.height)

              ctx.drawImage(img, -sw / 2 + w / 2, -sh / 2 + h / 2, img.width, img.height)
              ctx.fillStyle = 'white';
              ctx.fill();
              var imgData = ctx.getImageData(0, 0, width, height);
              var radius = that.data.radius
              var sigma = that.data.sigma
              var newImgData = gaussBlur1(imgData, ctx, radius, sigma)
              for(var i =0;i<imgData.data.length;i=i+4){
                newImgData.data[i] = parseInt(imgData.data[i] / newImgData.data[i] * 250)
                newImgData.data[i + 1] = parseInt(imgData.data[i + 1] / newImgData.data[i + 1] * 250)
                newImgData.data[i + 2] = parseInt(imgData.data[i + 2] / newImgData.data[i + 2] * 250)
    
                for(var j=0;j<3;j++){
                  if (newImgData.data[i+j]>255){
                    newImgData.data[i+j] = 255
                  }
                }
              }

              console.log(newImgData)

              ctx.putImageData(newImgData, 0, 0);
              console.log("convert ok!")
            }
            img.src = path
          })
      }
    })

  },
  linearTransform_gray: function () {
    var linear_table = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4,
      4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8,
      9, 9, 9, 9, 10, 10, 10, 10, 11, 11, 11, 11, 12, 12, 12, 12, 13, 13,
      13, 13, 14, 14, 14, 14, 15, 15, 15, 15, 16, 17, 19, 21, 23, 24, 26, 28,
      30, 31, 33, 35, 37, 38, 40, 42, 44, 45, 47, 49, 51, 52, 54, 56, 58, 59,
      61, 63, 65, 66, 68, 70, 72, 73, 75, 77, 79, 80, 82, 84, 86, 87, 89, 91,
      93, 94, 96, 98, 100, 101, 103, 105, 107, 108, 110, 112, 114, 115, 117, 119, 121, 122,
      124, 126, 128, 129, 131, 132, 134, 135, 137, 138, 140, 142, 143, 145, 146, 148, 149, 151,
      152, 154, 156, 157, 159, 160, 162, 163, 165, 166, 168, 170, 171, 173, 174, 176, 177, 179,
      180, 182, 184, 185, 187, 188, 190, 191, 193, 194, 196, 198, 199, 201, 202, 204, 205, 207,
      208, 210, 212, 213, 215, 216, 218, 219, 221, 222, 224, 226, 227, 229, 230, 232, 233, 235,
      236, 238, 240, 240, 240, 240, 241, 241, 241, 241, 242, 242, 242, 243, 243, 243, 243, 244,
      244, 244, 244, 245, 245, 245, 246, 246, 246, 246, 247, 247, 247, 247, 248, 248, 248, 249,
      249, 249, 249, 250, 250, 250, 250, 251, 251, 251, 252, 252, 252, 252, 253, 253, 253, 253,
      254, 254, 254, 255];
    var that = this;
    wx.getImageInfo({
      src: that.data.img,
      success: (imgInfo) => {
        let {
          width,
          height,
          imgPath
        } = imgInfo;
        var path = that.data.img
        wx.createSelectorQuery()
          .select('#canvas')
          .fields({
            node: true,
            size: true,
          })
          .exec((res) => {
            const canvas = res[0].node
            console.log(res[0])
            const ctx = canvas.getContext('2d')

            const img = canvas.createImage()
            img.onload = () => {
              var scale = 1.0
              var sw = img.width * scale
              var sh = img.height * scale

              var pixelRatio = 0
              wx.getSystemInfo({
                success: function (res) {
                  pixelRatio = res.pixelRatio
                },
                fail: function () {
                  pixelRatio = 0
                }
              })
              ctx.scale(pixelRatio, pixelRatio)
              canvas.width = img.width
              canvas.height = img.height
              var w = canvas.width;
              var h = canvas.height;
              ctx.clearRect(0, 0, img.width, img.height)

              ctx.drawImage(img, -sw / 2 + w / 2, -sh / 2 + h / 2, img.width, img.height)
              ctx.fillStyle = 'white';
              ctx.fill();
              var imgData = ctx.getImageData(0, 0, width, height);
              //变成灰度
              for (var i = 0; i < imgData.data.length; i += 4) {
                var gray = parseInt((imgData.data[i + 0] + imgData.data[i + 1] + imgData.data[i + 2]) / 3)
                imgData.data[i + 0] = gray;
                imgData.data[i + 1] = gray;
                imgData.data[i + 2] = gray;
                imgData.data[i + 3] = 255;
              }
              var newImgData = ctx.createImageData(width, height);

              for (var i = 0; i < imgData.data.length; i = i + 4) {
                newImgData.data[i] = linear_table[imgData.data[i]]
                newImgData.data[i + 1] = linear_table[imgData.data[i + 1]]
                newImgData.data[i + 2] = linear_table[imgData.data[i + 2]]
                newImgData.data[i + 3] = 255
              }

              ctx.putImageData(newImgData, 0, 0);
            }
            img.src = path
          })
      }
    })
  },
  histEqual_gray: function () {
    var that = this;
    wx.getImageInfo({
      src: that.data.img,
      success: (imgInfo) => {
        let {
          width,
          height,
          imgPath
        } = imgInfo;
        var path = that.data.img
        wx.createSelectorQuery()
          .select('#canvas')
          .fields({
            node: true,
            size: true,
          })
          .exec((res) => {
            const canvas = res[0].node
            console.log(res[0])
            const ctx = canvas.getContext('2d')

            const img = canvas.createImage()
            img.onload = () => {
              var scale = 1.0
              var sw = img.width * scale
              var sh = img.height * scale

              var pixelRatio = 0
              wx.getSystemInfo({
                success: function (res) {
                  pixelRatio = res.pixelRatio
                },
                fail: function () {
                  pixelRatio = 0
                }
              })
              ctx.scale(pixelRatio, pixelRatio)
              canvas.width = img.width
              canvas.height = img.height
              var w = canvas.width;
              var h = canvas.height;
              ctx.clearRect(0, 0, img.width, img.height)

              ctx.drawImage(img, -sw / 2 + w / 2, -sh / 2 + h / 2, img.width, img.height)
              ctx.fillStyle = 'white';
              ctx.fill();
              var imgData = ctx.getImageData(0, 0, width, height);
              //变成灰度
              for (var i = 0; i < imgData.data.length; i += 4) {
                var gray = parseInt((imgData.data[i + 0] + imgData.data[i + 1] + imgData.data[i + 2]) / 3)
                imgData.data[i + 0] = gray;
                imgData.data[i + 1] = gray;
                imgData.data[i + 2] = gray;
                imgData.data[i + 3] = 255;
              }
              var newImgData = ctx.createImageData(width, height);

              var hist_val = new Array(3 * 256)
              for (var i = 0; i < 3 * 256; i++) {
                hist_val[i] = 0
              }
              for (var i = 0; i < imgData.data.length; i = i + 4) {
                // 存储格式，前256为R，中为G，后为B
                hist_val[imgData.data[i]] += 1 / (width * height)
                hist_val[256 + imgData.data[i + 1]] += 1 / (width * height)
                hist_val[256 * 2 + imgData.data[i + 2]] += 1 / (width * height)
              }
              var hist_cdf = hist_val
              for (var i = 1; i < 256; i++) {
                hist_cdf[i] = hist_cdf[i] + hist_cdf[i - 1]
                hist_cdf[256 + i] = hist_cdf[256 + i] + hist_cdf[256 + i - 1]
                hist_cdf[256 * 2 + i] = hist_cdf[256 * 2 + i] + hist_cdf[256 * 2 + i - 1]
                hist_cdf[i - 1] = parseInt(255 * hist_cdf[i - 1] + 0.1)
                hist_cdf[256 + i - 1] = parseInt(255 * hist_cdf[256 + i - 1] + 0.1)
                hist_cdf[256 * 2 + i - 1] = parseInt(255 * hist_cdf[256 * 2 + i - 1] + 0.1)
              }
              hist_cdf[255] = parseInt(255 * hist_cdf[255] + 0.1)
              hist_cdf[255 + 256] = parseInt(255 * hist_cdf[255 + 256] + 0.1)
              hist_cdf[255 + 256 * 2] = parseInt(255 * hist_cdf[255 + 256 * 2] + 0.1)
              for (var i = 0; i < newImgData.data.length; i = i + 4) {
                newImgData.data[i] = hist_cdf[imgData.data[i]]
                newImgData.data[i + 1] = hist_cdf[256 + imgData.data[i + 1]]
                newImgData.data[i + 2] = hist_cdf[256 * 2 + imgData.data[i + 2]]
                newImgData.data[i + 3] = 255
              }

              ctx.putImageData(newImgData, 0, 0);
            }
            img.src = path
          })
      }
    })
  },
  sharpen_gray: function () {
    var that = this;
    wx.getImageInfo({
      src: that.data.img,
      success: (imgInfo) => {
        let {
          width,
          height,
          imgPath
        } = imgInfo;
        var path = that.data.img
        wx.createSelectorQuery()
          .select('#canvas')
          .fields({
            node: true,
            size: true,
          })
          .exec((res) => {
            const canvas = res[0].node
            console.log(res[0])
            const ctx = canvas.getContext('2d')

            const img = canvas.createImage()
            img.onload = () => {
              var scale = 1.0
              var sw = img.width * scale
              var sh = img.height * scale

              var pixelRatio = 0
              wx.getSystemInfo({
                success: function (res) {
                  pixelRatio = res.pixelRatio
                },
                fail: function () {
                  pixelRatio = 0
                }
              })
              ctx.scale(pixelRatio, pixelRatio)
              canvas.width = img.width
              canvas.height = img.height
              var w = canvas.width;
              var h = canvas.height;
              ctx.clearRect(0, 0, img.width, img.height)

              ctx.drawImage(img, -sw / 2 + w / 2, -sh / 2 + h / 2, img.width, img.height)
              ctx.fillStyle = 'white';
              ctx.fill();
              var imgData = ctx.getImageData(0, 0, width, height);
              //变成灰度
              for (var i = 0; i < imgData.data.length; i += 4) {
                var gray = parseInt((imgData.data[i + 0] + imgData.data[i + 1] + imgData.data[i + 2]) / 3)
                imgData.data[i + 0] = gray;
                imgData.data[i + 1] = gray;
                imgData.data[i + 2] = gray;
                imgData.data[i + 3] = 255;
              }
              var newImgData = ctx.createImageData(width, height);

              var kernel = [0, -1, 0, -1, 5, -1, 0, -1, 0] //参数
              var ksize = parseInt(Math.sqrt(kernel.length))
              var border = parseInt(ksize / 2)
              var counts = 0
              var skip_counts = 0
              for (var i = 0; i < imgData.data.length; i = i + 4) {

                var index_height = parseInt(counts / width)
                var index_width = counts % width
                if (index_height < border || index_height >= height - border || index_width < border || index_width >= width - border) {
                  newImgData.data[i] = imgData.data[i]
                  newImgData.data[i + 1] = imgData.data[i + 1]
                  newImgData.data[i + 2] = imgData.data[i + 2]
                  newImgData.data[i + 3] = 255
                  skip_counts += 1
                  counts += 1
                  continue
                }
                var sum = [0, 0, 0]
                for (var j = 0; j < kernel.length; j++) {
                  var index_kernal_x = parseInt(j / ksize)
                  var index_kernal_y = j % ksize - (ksize - 1) / 2
                  sum[0] += kernel[j] * imgData.data[i + index_kernal_x * 4 * width + 4 * index_kernal_y]
                  sum[1] += kernel[j] * imgData.data[i + 1 + index_kernal_x * 4 * width + 4 * index_kernal_y]
                  sum[2] += kernel[j] * imgData.data[i + 2 + index_kernal_x * 4 * width + 4 * index_kernal_y]
                }
                newImgData.data[i] = sum[0]
                newImgData.data[i + 1] = sum[1]
                newImgData.data[i + 2] = sum[2]
                newImgData.data[i + 3] = 255

                counts += 1
              }
              console.log(skip_counts)

              ctx.putImageData(newImgData, 0, 0);
            }
            img.src = path
          })
      }
    })
  },
  usm_gray: function () {
    function gaussBlur1(imgData, ctx, radius, sigma) {
      var pixes = imgData.data;
      var width = imgData.width;
      var height = imgData.height;
      var newImgData = ctx.createImageData(width, height);
      var gaussMatrix = [],
        gaussSum = 0,
        x, y,
        r, g, b, a,
        i, j, k, len;


      radius = Math.floor(radius) || 3;
      sigma = sigma || radius / 3;

      a = 1 / (Math.sqrt(2 * Math.PI) * sigma);
      b = -1 / (2 * sigma * sigma);
      //生成高斯矩阵
      for (i = 0, x = -radius; x <= radius; x++ , i++) {
        g = a * Math.exp(b * x * x);
        gaussMatrix[i] = g;
        gaussSum += g;

      }
      //归一化, 保证高斯矩阵的值在[0,1]之间
      for (i = 0, len = gaussMatrix.length; i < len; i++) {
        gaussMatrix[i] /= gaussSum;
      }
      //x 方向一维高斯运算
      for (y = 0; y < height; y++) {
        for (x = 0; x < width; x++) {
          r = g = b = a = 0;
          gaussSum = 0;
          for (j = -radius; j <= radius; j++) {
            k = x + j;
            if (k >= 0 && k < width) {//确保 k 没超出 x 的范围
              //r,g,b,a 四个一组
              i = (y * width + k) * 4;
              r += pixes[i] * gaussMatrix[j + radius];
              g += pixes[i + 1] * gaussMatrix[j + radius];
              b += pixes[i + 2] * gaussMatrix[j + radius];
              // a += pixes[i + 3] * gaussMatrix[j];
              gaussSum += gaussMatrix[j + radius];
            }
          }
          i = (y * width + x) * 4;
          // 除以 gaussSum 是为了消除处于边缘的像素, 高斯运算不足的问题
          newImgData.data[i] = r / gaussSum
          newImgData.data[i + 1] = g / gaussSum;
          newImgData.data[i + 2] = b / gaussSum;
          newImgData.data[i + 3] = 255

        }
      }
      //y 方向一维高斯运算
      for (x = 0; x < width; x++) {
        for (y = 0; y < height; y++) {
          r = g = b = a = 0;
          gaussSum = 0;
          for (j = -radius; j <= radius; j++) {
            k = y + j;
            if (k >= 0 && k < height) {//确保 k 没超出 y 的范围
              i = (k * width + x) * 4;
              r += newImgData.data[i] * gaussMatrix[j + radius];
              g += newImgData.data[i + 1] * gaussMatrix[j + radius];
              b += newImgData.data[i + 2] * gaussMatrix[j + radius];
              // a += pixes[i + 3] * gaussMatrix[j];
              gaussSum += gaussMatrix[j + radius];
            }
          }
          i = (y * width + x) * 4;
          newImgData.data[i] = r / gaussSum
          newImgData.data[i + 1] = g / gaussSum;
          newImgData.data[i + 2] = b / gaussSum;
          newImgData.data[i + 3] = 255
        }
      }
      //end
      return newImgData;
    }

    // 正式运行
    var that = this;
    wx.getImageInfo({
      src: that.data.img,
      success: (imgInfo) => {
        let {
          width,
          height,
          imgPath
        } = imgInfo;
        var path = that.data.img
        wx.createSelectorQuery()
          .select('#canvas')
          .fields({
            node: true,
            size: true,
          })
          .exec((res) => {
            const canvas = res[0].node
            console.log(res[0])
            const ctx = canvas.getContext('2d')

            const img = canvas.createImage()
            img.onload = () => {
              var scale = 1.0
              var sw = img.width * scale
              var sh = img.height * scale

              var pixelRatio = 0
              wx.getSystemInfo({
                success: function (res) {
                  pixelRatio = res.pixelRatio
                },
                fail: function () {
                  pixelRatio = 0
                }
              })
              ctx.scale(pixelRatio, pixelRatio)
              canvas.width = img.width
              canvas.height = img.height
              var w = canvas.width;
              var h = canvas.height;
              ctx.clearRect(0, 0, img.width, img.height)

              ctx.drawImage(img, -sw / 2 + w / 2, -sh / 2 + h / 2, img.width, img.height)
              ctx.fillStyle = 'white';
              ctx.fill();
              var k = that.data.usm_k_gray
              var radius = that.data.radius_gray
              var sigma = that.data.sigma_gray
              var imgData = ctx.getImageData(0, 0, width, height);
              //变成灰度
              for (var i = 0; i < imgData.data.length; i += 4) {
                var gray = parseInt((imgData.data[i + 0] + imgData.data[i + 1] + imgData.data[i + 2]) / 3)
                imgData.data[i + 0] = gray;
                imgData.data[i + 1] = gray;
                imgData.data[i + 2] = gray;
                imgData.data[i + 3] = 255;
              }
              var newImgData = gaussBlur1(imgData, ctx, radius, sigma)
              for (var i = 0; i < imgData.data.length; i = i + 4) {
                newImgData.data[i] = parseInt((1 + k) * imgData.data[i] - k * newImgData.data[i])
                newImgData.data[i + 1] = parseInt((1 + k) * imgData.data[i + 1] - k * newImgData.data[i + 1])
                newImgData.data[i + 2] = parseInt((1 + k) * imgData.data[i + 2] - k * newImgData.data[i + 2])
              }

              ctx.putImageData(newImgData, 0, 0);
              console.log("convert ok!")
            }
            img.src = path
          })
      }
    })
  },
  gaussianFilter_gray: function () {
    function gaussBlur1(imgData, ctx, radius, sigma) {
      var pixes = imgData.data;
      var width = imgData.width;
      var height = imgData.height;
      var newImgData = ctx.createImageData(width, height);
      var gaussMatrix = [],
        gaussSum = 0,
        x, y,
        r, g, b, a,
        i, j, k, len;


      radius = Math.floor(radius) || 3;
      sigma = sigma || radius / 3;

      a = 1 / (Math.sqrt(2 * Math.PI) * sigma);
      b = -1 / (2 * sigma * sigma);
      //生成高斯矩阵
      for (i = 0, x = -radius; x <= radius; x++ , i++) {
        g = a * Math.exp(b * x * x);
        gaussMatrix[i] = g;
        gaussSum += g;

      }
      //归一化, 保证高斯矩阵的值在[0,1]之间
      for (i = 0, len = gaussMatrix.length; i < len; i++) {
        gaussMatrix[i] /= gaussSum;
      }
      //x 方向一维高斯运算
      for (y = 0; y < height; y++) {
        for (x = 0; x < width; x++) {
          r = g = b = a = 0;
          gaussSum = 0;
          for (j = -radius; j <= radius; j++) {
            k = x + j;
            if (k >= 0 && k < width) {//确保 k 没超出 x 的范围
              //r,g,b,a 四个一组
              i = (y * width + k) * 4;
              r += pixes[i] * gaussMatrix[j + radius];
              g += pixes[i + 1] * gaussMatrix[j + radius];
              b += pixes[i + 2] * gaussMatrix[j + radius];
              // a += pixes[i + 3] * gaussMatrix[j];
              gaussSum += gaussMatrix[j + radius];
            }
          }
          i = (y * width + x) * 4;
          // 除以 gaussSum 是为了消除处于边缘的像素, 高斯运算不足的问题
          // console.log(gaussSum)
          pixes[i] = r / gaussSum;
          pixes[i + 1] = g / gaussSum;
          pixes[i + 2] = b / gaussSum;
          newImgData.data[i] = pixes[i]
          newImgData.data[i + 1] = pixes[i + 1]
          newImgData.data[i + 2] = pixes[i + 2]
          newImgData.data[i + 3] = 255

          // pixes[i + 3] = a ;
        }
      }
      //y 方向一维高斯运算
      for (x = 0; x < width; x++) {
        for (y = 0; y < height; y++) {
          r = g = b = a = 0;
          gaussSum = 0;
          for (j = -radius; j <= radius; j++) {
            k = y + j;
            if (k >= 0 && k < height) {//确保 k 没超出 y 的范围
              i = (k * width + x) * 4;
              r += pixes[i] * gaussMatrix[j + radius];
              g += pixes[i + 1] * gaussMatrix[j + radius];
              b += pixes[i + 2] * gaussMatrix[j + radius];
              // a += pixes[i + 3] * gaussMatrix[j];
              gaussSum += gaussMatrix[j + radius];
            }
          }
          i = (y * width + x) * 4;
          pixes[i] = r / gaussSum;
          pixes[i + 1] = g / gaussSum;
          pixes[i + 2] = b / gaussSum;
          newImgData.data[i] = pixes[i]
          newImgData.data[i + 1] = pixes[i + 1]
          newImgData.data[i + 2] = pixes[i + 2]
          newImgData.data[i + 3] = 255
          // pixes[i] = r ;
          // pixes[i + 1] = g ;
          // pixes[i + 2] = b ;
          // pixes[i + 3] = a ;
        }
      }
      //end
      // newImgData.data = pixes;
      return newImgData;
    }

    // 正式运行
    var that = this;
    wx.getImageInfo({
      src: that.data.img,
      success: (imgInfo) => {
        let {
          width,
          height,
          imgPath
        } = imgInfo;
        var path = that.data.img
        wx.createSelectorQuery()
          .select('#canvas')
          .fields({
            node: true,
            size: true,
          })
          .exec((res) => {
            const canvas = res[0].node
            console.log(res[0])
            const ctx = canvas.getContext('2d')

            const img = canvas.createImage()
            img.onload = () => {
              var scale = 1.0
              var sw = img.width * scale
              var sh = img.height * scale

              var pixelRatio = 0
              wx.getSystemInfo({
                success: function (res) {
                  pixelRatio = res.pixelRatio
                },
                fail: function () {
                  pixelRatio = 0
                }
              })
              ctx.scale(pixelRatio, pixelRatio)
              canvas.width = img.width
              canvas.height = img.height
              var w = canvas.width;
              var h = canvas.height;
              ctx.clearRect(0, 0, img.width, img.height)

              ctx.drawImage(img, -sw / 2 + w / 2, -sh / 2 + h / 2, img.width, img.height)
              ctx.fillStyle = 'white';
              ctx.fill();
              var imgData = ctx.getImageData(0, 0, width, height);
              //变成灰度
              for (var i = 0; i < imgData.data.length; i += 4) {
                var gray = parseInt((imgData.data[i + 0] + imgData.data[i + 1] + imgData.data[i + 2]) / 3)
                imgData.data[i + 0] = gray;
                imgData.data[i + 1] = gray;
                imgData.data[i + 2] = gray;
                imgData.data[i + 3] = 255;
              }
              var radius = that.data.radius_gray
              var sigma = that.data.sigma_gray
              var newImgData = gaussBlur1(imgData, ctx, radius, sigma)

              ctx.putImageData(newImgData, 0, 0);
              console.log("convert ok!")
            }
            img.src = path
          })
      }
    })

  },
  removeShadow_gray: function () {
    function gaussBlur1(imgData, ctx, radius, sigma) {
      var pixes = imgData.data;
      var width = imgData.width;
      var height = imgData.height;
      var newImgData = ctx.createImageData(width, height);
      var gaussMatrix = [],
        gaussSum = 0,
        x, y,
        r, g, b, a,
        i, j, k, len;
      radius = Math.floor(radius) || 3;
      sigma = sigma || radius / 3;

      a = 1 / (Math.sqrt(2 * Math.PI) * sigma);
      b = -1 / (2 * sigma * sigma);
      //生成高斯矩阵
      for (i = 0, x = -radius; x <= radius; x++ , i++) {
        g = a * Math.exp(b * x * x);
        gaussMatrix[i] = g;
        gaussSum += g;

      }
      //归一化, 保证高斯矩阵的值在[0,1]之间
      for (i = 0, len = gaussMatrix.length; i < len; i++) {
        gaussMatrix[i] /= gaussSum;
      }
      //x 方向一维高斯运算
      for (y = 0; y < height; y++) {
        for (x = 0; x < width; x++) {
          r = g = b = a = 0;
          gaussSum = 0;
          for (j = -radius; j <= radius; j++) {
            k = x + j;
            if (k >= 0 && k < width) {//确保 k 没超出 x 的范围
              //r,g,b,a 四个一组
              i = (y * width + k) * 4;
              r += pixes[i] * gaussMatrix[j + radius];
              g += pixes[i + 1] * gaussMatrix[j + radius];
              b += pixes[i + 2] * gaussMatrix[j + radius];
              // a += pixes[i + 3] * gaussMatrix[j];
              gaussSum += gaussMatrix[j + radius];
            }
          }
          i = (y * width + x) * 4;
          // 除以 gaussSum 是为了消除处于边缘的像素, 高斯运算不足的问题
          newImgData.data[i] = r / gaussSum
          newImgData.data[i + 1] = g / gaussSum;
          newImgData.data[i + 2] = b / gaussSum;
          newImgData.data[i + 3] = 255

          // pixes[i + 3] = a ;
        }
      }
      //y 方向一维高斯运算
      for (x = 0; x < width; x++) {
        for (y = 0; y < height; y++) {
          r = g = b = a = 0;
          gaussSum = 0;
          for (j = -radius; j <= radius; j++) {
            k = y + j;
            if (k >= 0 && k < height) {//确保 k 没超出 y 的范围
              i = (k * width + x) * 4;
              r += newImgData.data[i] * gaussMatrix[j + radius];
              g += newImgData.data[i + 1] * gaussMatrix[j + radius];
              b += newImgData.data[i + 2] * gaussMatrix[j + radius];
              gaussSum += gaussMatrix[j + radius];
            }
          }
          i = (y * width + x) * 4;
          newImgData.data[i] = r / gaussSum
          newImgData.data[i + 1] = g / gaussSum;
          newImgData.data[i + 2] = b / gaussSum;
          newImgData.data[i + 3] = 255
        }
      }
      return newImgData;
    }

    // 正式运行
    var that = this;
    wx.getImageInfo({
      src: that.data.img,
      success: (imgInfo) => {
        let {
          width,
          height,
          imgPath
        } = imgInfo;
        var path = that.data.img
        wx.createSelectorQuery()
          .select('#canvas')
          .fields({
            node: true,
            size: true,
          })
          .exec((res) => {
            const canvas = res[0].node
            console.log(res[0])
            const ctx = canvas.getContext('2d')

            const img = canvas.createImage()
            img.onload = () => {
              var scale = 1.0
              var sw = img.width * scale
              var sh = img.height * scale

              var pixelRatio = 0
              wx.getSystemInfo({
                success: function (res) {
                  pixelRatio = res.pixelRatio
                },
                fail: function () {
                  pixelRatio = 0
                }
              })
              ctx.scale(pixelRatio, pixelRatio)
              canvas.width = img.width
              canvas.height = img.height
              var w = canvas.width;
              var h = canvas.height;
              ctx.clearRect(0, 0, img.width, img.height)

              ctx.drawImage(img, -sw / 2 + w / 2, -sh / 2 + h / 2, img.width, img.height)
              ctx.fillStyle = 'white';
              ctx.fill();
              var imgData = ctx.getImageData(0, 0, width, height);
              //变成灰度
              for (var i = 0; i < imgData.data.length; i += 4) {
                var gray = parseInt((imgData.data[i + 0] + imgData.data[i + 1] + imgData.data[i + 2]) / 3)
                imgData.data[i + 0] = gray;
                imgData.data[i + 1] = gray;
                imgData.data[i + 2] = gray;
                imgData.data[i + 3] = 255;
              }
              var radius = that.data.radius_gray
              var sigma = that.data.sigma_gray
              var newImgData = gaussBlur1(imgData, ctx, radius, sigma)
              for (var i = 0; i < imgData.data.length; i = i + 4) {
                newImgData.data[i] = parseInt(imgData.data[i] / newImgData.data[i] * 250)
                newImgData.data[i + 1] = parseInt(imgData.data[i + 1] / newImgData.data[i + 1] * 250)
                newImgData.data[i + 2] = parseInt(imgData.data[i + 2] / newImgData.data[i + 2] * 250)

                for (var j = 0; j < 3; j++) {
                  if (newImgData.data[i + j] > 255) {
                    newImgData.data[i + j] = 255
                  }
                }
              }
              console.log(newImgData)

              ctx.putImageData(newImgData, 0, 0);
              console.log("convert ok!")
            }
            img.src = path
          })
      }
    })

  },
  block_height: function (event) {
    var that = this;
    that.setData({
      block_height: event.detail
    })
  },
  block_width:function(event){
    var that = this;
    that.setData({
      block_width:event.detail
    })
  },
  move_n:function(event){
    var that = this;
    that.setData({
      move_n: event.detail
    })
  },
  move_b: function (event) {
    var that = this;
    that.setData({
      move_b: event.detail
    })
  },
  radius_gray:function(event){
    var that = this;
    that.setData({
      radius_gray: event.detail
    })
  },
  sigma_gray: function (event) {
    var that = this;
    that.setData({
      sigma_gray: event.detail
    })
  },
  radius: function (event) {
    var that = this;
    that.setData({
      radius: event.detail
    })
  },
  sigma: function (event) {
    var that = this;
    that.setData({
      sigma: event.detail
    })
  },
  usm_k:function(event){
    var that = this;
    that.setData({
      usm_k: event.detail
    })
  },
  usm_k_gray: function (event) {
    var that = this;
    that.setData({
      usm_k_gray: event.detail
    })
  }

})
