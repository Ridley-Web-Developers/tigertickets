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
        component: () => import('../views/about/Main.vue')
    },
    {
        path: '/about/team',
        name: 'Team',
        component: () => import('../views/about/Team.vue')
    },
    {
        path: '/about/projects',
        name: 'Projects',
        component: () => import('../views/about/Projects.vue')
    },
    {
        path: '/about/theatre',
        name: 'Mandeville Theatre',
        component: () => import('../views/about/Theatre.vue')
    },
    {
        path: '/events',
        name: 'Events',
        component: () => import('../views/events/Main.vue')
    },
    {
        path: '/events/:id',
        name: 'Event',
        component: () => import('../views/events/Event.vue')
    },
    {
        path: '/events/all',
        name: 'All Events',
        component: () => import('../views/events/All Events.vue')
    },
    {
        path: '*',
        redirect:
            {
                name: 'Home'
            }
    }

]

const router = new VueRouter({
    routes
})

export default router
