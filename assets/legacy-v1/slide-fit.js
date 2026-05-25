// Scale a .slide (1920x1080) to fit the viewport while preserving aspect ratio.
(function () {
  function fit() {
    const slide = document.querySelector('.slide');
    if (!slide) return;
    const scale = Math.min(
      window.innerWidth / 1920,
      window.innerHeight / 1080
    );
    slide.style.transform = `scale(${scale})`;
  }
  window.addEventListener('resize', fit);
  window.addEventListener('load', fit);
  fit();
})();
