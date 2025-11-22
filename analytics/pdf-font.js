// pdf-font.js – один раз на весь сайт
(function () {
    if (window.pdfCyrillicReady) return;
  
    const fontUrl = 'https://cdnjs.cloudflare.com/ajax/libs/pdf-make/0.2.7/fonts/Roboto-Regular.ttf';
  
    fetch(fontUrl)
      .then(r => r.arrayBuffer())
      .then(buffer => {
        const { jsPDF } = window.jspdf;
        const base64 = btoa(String.fromCharCode(...new Uint8Array(buffer)));
  
        jsPDF.API.addFileToVFS('Roboto.ttf', base64);
        jsPDF.API.addFont('Roboto.ttf', 'Roboto', 'normal');
  
        window.pdfCyrillicReady = true;
        console.log('Шрифт Roboto для PDF загружен');
      })
      .catch(err => console.error('Не удалось загрузить шрифт для PDF:', err));
  })();