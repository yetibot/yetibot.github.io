(ns ok.data.docs
  (:require [ok.layout :as layout]))

(defn- project
  [project]
  (prn project)
  [:li [:a {:href (str "/doc/" (name (:key project)) ".html")}
        [:p.name (:name project)]
        (if-let [image (:image project)]
          [:img.project-thumb {:src image}])]])


(defn- sort-projects
  [projects]
  (->> projects
       (map #(assoc (last %) :key (first %)))
       (sort-by #(or (:priority %) 9999))))

(defn page
  [arg]
  (let [db (get-in arg [:meta :fsdb :manifest])
        projects (sort-projects (-> db :projects))
        disclosed (filter :name (-> projects))
        num-undisclosed (- (count projects) (count disclosed))]
    (layout/main arg
                 [:main.projects
                  [:h1 "THE docs"]
                  [:ul.projects-list
                   (map project (filter #(contains? % :name) projects))]
                  [:h3 "and " num-undisclosed " undisclosed."]])))
