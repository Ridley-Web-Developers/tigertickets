import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/about',
        name: 'About',
        component: () => import('../views/About.vue')
    },
    {
        path: '/about/developers',
        name: 'Developers',
        component: () => import('../views/Developer.vue')
    },
    {
        path: '/theatre',
        name: 'Mandeville Theatre',
        component: () => import('../views/Theatre.vue')
    },
    {
        path: '/events',
        name: 'Events',
        component: () => import('../views/Events.vue')
    },
    {
        path: '/events/:id',
        name: 'Event',
        component: () => import('../views/Event.vue')
    },
    {
        path: '/events/all',
        name: 'All Events',
        component: () => import('../views/All Events.vue')
    }
]

const router = new VueRouter({
    routes
})

export default router
