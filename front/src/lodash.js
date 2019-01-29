// cherry-pick specific lodash methods here to reduce bundle size

export default {
  clone: require('lodash/clone'),
  debounce: require('lodash/debounce'),
  get: require('lodash/get'),
  merge: require('lodash/merge'),
  range: require('lodash/range'),
  shuffle: require('lodash/shuffle'),
  sortBy: require('lodash/sortBy'),
  throttle: require('lodash/throttle'),
  uniq: require('lodash/uniq'),
}