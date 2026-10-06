// Configuración de 11ty — sitio Diforza
// Fuente: src/  ·  Salida (lo que se publica en Cloudflare Pages): _site/
module.exports = function (eleventyConfig) {
  // Archivos que se copian tal cual (no se procesan como plantillas)
  eleventyConfig.addPassthroughCopy("src/assets");   // CSS y JS
  eleventyConfig.addPassthroughCopy("src/img");      // imágenes compartidas
  eleventyConfig.addPassthroughCopy("src/*/img");    // imágenes propias de cada landing

  eleventyConfig.addWatchTarget("src/assets/");

  return {
    dir: {
      input: "src",
      includes: "_includes",
      data: "_data",
      output: "_site",
    },
    templateFormats: ["njk", "md"],
    htmlTemplateEngine: "njk",
    markdownTemplateEngine: "njk",
  };
};
