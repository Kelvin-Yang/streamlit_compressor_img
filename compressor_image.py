import streamlit as st
import streamlit.components.v1 as components

# Streamlit 页面设置
st.set_page_config(page_title="Image Compression with Compressor.js", layout="centered")

# 插入 HTML 和 JavaScript
components.html(
    """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.jsdelivr.net/npm/compressorjs@1.2.1/dist/compressor.min.js"></script>
    </head>
    <body>
        <input type="file" id="upload" accept="image/*" style="margin-bottom: 20px;">
        <button id="download" style="display:none; margin-top: 20px;">Download Compressed Image</button>
        <p id="status"></p>
        <script>
            const upload = document.getElementById('upload');
            const download = document.getElementById('download');
            const status = document.getElementById('status');
            let compressedBlobUrl = null;

            upload.addEventListener('change', function(event) {
                const file = event.target.files[0];

                if (!file) {
                    status.textContent = "No file selected.";
                    return;
                }

                // 显示正在压缩的状态
                status.textContent = "Compressing...";

                new Compressor(file, {
                    quality: 0.6, // 压缩质量（0 到 1 之间）
                    success(result) {
                        status.textContent = "Compression successful!";
                        
                        if (compressedBlobUrl) {
                            URL.revokeObjectURL(compressedBlobUrl); // 释放之前的 Blob URL
                        }

                        compressedBlobUrl = URL.createObjectURL(result);

                        // 设置下载链接和文件名
                        download.style.display = 'inline';
                        download.href = compressedBlobUrl;
                        download.download = file.name.split('.')[0] + '_compressed.' + result.type.split('/')[1];
                        download.textContent = 'Download ' + download.download;

                        // 绑定点击事件并强制下载
                        download.onclick = function() {
                            const link = document.createElement('a');
                            link.href = compressedBlobUrl;
                            link.download = download.download;
                            link.click();
                        };
                    },
                    error(err) {
                        console.error(err.message);
                        status.textContent = "Compression failed!";
                    },
                });
            });
        </script>
    </body>
    </html>
    """,
    height=500,
)
