module.exports = {
  async onPreBuild({ utils }) {
    await utils.cache.restore("./bin/blog");
  },
  async onPostBuild({ utils }) {
    await utils.cache.save("./bin/blog", {
      digests: ["./VERSION"],
    });
  },
};
