import { createRouter, createWebHistory } from "vue-router";

const routes = [
    {
        path: "/",
        name: "Home",
        component: () => import("@/views/Home.vue"),
        children: [
            {
                name: 'stock',
                path: "/:id",
                component: () => import("@/views/Stock.vue")
            },
        ]
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
