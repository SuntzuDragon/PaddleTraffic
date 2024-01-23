import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import MapView from '../views/MapView.vue'
import MatchView from '../views/MatchView.vue'
import LoginView from '../views/LoginView.vue'

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView
        },
        {
            path: '/about',
            name: 'about',
            component: AboutView
        },
        {
            path: '/map',
            name: 'map',
            component: MapView
        },
        {
            path: '/matchmaking',
            name: 'matchmaking',
            component: MatchView
        },
        {
            path: '/login',
            name: 'login page',
            component: LoginView
        },
    ]
})

export default router