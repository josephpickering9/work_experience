module.exports = {
  apps: [
    {
      name: 'WorkExperienceWeb',
      port: '3000',
      exec_mode: 'cluster',
      instances: 'max',
      interpreter: '/usr/bin/node',
      script: './.output/server/index.mjs',
      node_args: '--loader ts-node/esm',
      env: {
        NODE_OPTIONS: '--experimental-specifier-resolution=node',
      },
    },
  ],
}
