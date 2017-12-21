(ns ok.data.index
  (:require [ok.layout :as layout]))

(defn page [arg]
  (let [db (get-in arg [:meta :fsdb :manifest])
        num-people      (-> db :people count)
        num-techs       (-> db :technologies count)
        num-clients     (-> db :clients count)
        num-services    (-> db :services count)
        num-projects    (-> db :projects count)
        num-docs        (-> db :docs count)
        ;;num-plugins     ("42")
        num-opensourced (->> db :projects vals (filter :opensourced) count)]
    (layout/main
     arg
     [:main.teaser-wrapper
      [:div.teaser
       [:span
        [:span "You can see Yetibot as a communal command line (*). It supports "]
         [:a {:href "people.html"}
         num-people " databases"]]
       [:span
        [:span ", "]
        [:a {:href "#"}
          "over 9000 custom commands,"]]
       [:span
        [:span " working with "]
        [:a {:href "#"}
         num-services " APIs,"]]
       [:span
        [:span " and "]
        [:a {:href "#"}
         "an unlimited number of custom observers."]]
       [:div.supporting
        "* works with Slack and IRC... and it's Docker ready"]]])))
