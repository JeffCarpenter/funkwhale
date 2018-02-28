import axios from 'axios'
import jwtDecode from 'jwt-decode'
import logger from '@/logging'
import router from '@/router'

export default {
  namespaced: true,
  state: {
    authenticated: false,
    username: '',
    availablePermissions: {},
    profile: null,
    token: '',
    tokenData: {}
  },
  getters: {
    header: state => {
      return 'JWT ' + state.token
    }
  },
  mutations: {
    profile: (state, value) => {
      state.profile = value
    },
    authenticated: (state, value) => {
      state.authenticated = value
      if (value === false) {
        state.username = null
        state.token = null
        state.tokenData = null
        state.profile = null
        state.availablePermissions = {}
      }
    },
    username: (state, value) => {
      state.username = value
    },
    token: (state, value) => {
      state.token = value
      if (value) {
        state.tokenData = jwtDecode(value)
      } else {
        state.tokenData = {}
      }
    },
    permission: (state, {key, status}) => {
      state.availablePermissions[key] = status
    }
  },
  actions: {
    // Send a request to the login URL and save the returned JWT
    login ({commit, dispatch}, {next, credentials, onError}) {
      return axios.post('token/', credentials).then(response => {
        logger.default.info('Successfully logged in as', credentials.username)
        commit('token', response.data.token)
        commit('username', credentials.username)
        commit('authenticated', true)
        dispatch('fetchProfile')
        // Redirect to a specified route
        router.push(next)
      }, response => {
        logger.default.error('Error while logging in', response.data)
        onError(response)
      })
    },
    logout ({commit}) {
      commit('authenticated', false)
      logger.default.info('Log out, goodbye!')
      router.push({name: 'index'})
    },
    check ({commit, dispatch, state}) {
      logger.default.info('Checking authentication...')
      var jwt = state.token
      var username = state.username
      if (jwt) {
        commit('authenticated', true)
        commit('username', username)
        commit('token', jwt)
        logger.default.info('Logged back in as ' + username)
        dispatch('fetchProfile')
        dispatch('refreshToken')
      } else {
        logger.default.info('Anonymous user')
        commit('authenticated', false)
      }
    },
    fetchProfile ({commit, dispatch, state}) {
      return axios.get('users/users/me/').then((response) => {
        logger.default.info('Successfully fetched user profile')
        let data = response.data
        commit('profile', data)
        commit('username', data.username)
        dispatch('favorites/fetch', null, {root: true})
        Object.keys(data.permissions).forEach(function (key) {
          // this makes it easier to check for permissions in templates
          commit('permission', {key, status: data.permissions[String(key)].status})
        })
        return response.data
      }, (response) => {
        logger.default.info('Error while fetching user profile')
      })
    },
    refreshToken ({commit, dispatch, state}) {
      return axios.post('token/refresh/', {token: state.token}).then(response => {
        logger.default.info('Refreshed auth token')
        commit('token', response.data.token)
      }, response => {
        logger.default.error('Error while refreshing token', response.data)
      })
    }
  }
}