module.exports = function (eleventyConfig) {
  eleventyConfig.addPassthroughCopy("src/css");
  eleventyConfig.addPassthroughCopy("src/assets");

  eleventyConfig.addFilter("toBaseUrl", (path) => {
    const base = process.env.ELEVENTY_BASE_URL;
    if (!base) return path;
    return path.startsWith("/") ? base + path : path;
  });

  return {
    dir: {
      input: "src",
      output: "_site"
    },
  };
};
