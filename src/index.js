import ifIsImage from 'if-is-image';
import tocbot from 'tocbot';
import gql from 'graphql-tag';
// graphql.js docs https://graphql.org/graphql-js/graphql/
// import { request, GraphQLClient } from 'graphql-request'
// const client = graphql("https://public.yetibot.com/graphql");
import ApolloClient from "apollo-boost";
import {GitHubOrg} from 'github-org-cards'
import ReactDOM from 'react-dom';
import React from 'react';

// Team for Community page
const team = document.querySelector('.core-team');
if (team) {
  const GitHubOrgFactory = React.createFactory(GitHubOrg);
  ReactDOM.render(GitHubOrgFactory({org: 'yetibot', columns: 6}), team);
}

const endpoint = "https://public.yetibot.com/graphql";
// const endpoint = "http://localhost:3003/graphql";
const client = new ApolloClient({uri: endpoint});

// TOC interactive - desktop only for now
const toc = document.querySelector('.toc.column .content');
console.log(toc);
if (toc) {
  if (window.innerWidth > 768) {
    tocbot.init({
      tocSelector: '.toc .content',
      contentSelector: '.main-content',
      // Which headings to grab inside of the contentSelector element.
      headingSelector: 'h1, h2, h3, h4',
      positionFixedSelector: '.toc.column .content',
      positionFixedClass: 'fixed',
      fixedSidebarOffset: 230,
      headingsOffset: -15
    });
  }
  toc.classList.add('ready');
}


// Eval against Yetibot GraphQL
const evalQuery = gql`
  query EvalQuery($expr: String!) {
    eval(expr: $expr)
  }
`;

export const yetibotEval = function(expr) {
  console.log('eval', evalQuery, {expr});
  // '{eval(expr: "' + escape(expr) + '")}'
  // const result = client.request(evalQuery, {expr});
  return client.query({query: evalQuery, fetchPolicy: 'no-cache', variables: {expr}});
};


// Either prints raw text or images depending on url structure
const appendResult = async (response, node) => {
  // console.log(node, typeof(node), 'result', response, ifIsImage(response));
  // node.appendChild(document.createElement('br'));
  if (ifIsImage(response)) {
    const img = document.createElement("img");
    img.src = response;
    node.appendChild(img);
  } else {
    const span = document.createElement('span');
    span.className = 'wrap';
    span.append(`${response}\n`)
    node.append(span);
  }
};

// Init
document.addEventListener('DOMContentLoaded', function () {

  const codeBlocks = document.querySelectorAll('code.yetibot');
  codeBlocks.forEach(function(codeBlock) {

    const expr = codeBlock.textContent.trim().replace(/^!/, "");
    const runButton = document.createElement('a');
    runButton.setAttribute("class", "eval-button button is-info is-pulled-right");
    runButton.appendChild(document.createTextNode("Run"));
    runButton.onclick = function(e) {
      console.log('clicked', expr);
      const result = yetibotEval(expr);
      result.then(function(response) {
        console.log('result', response.data.eval);
        response.data.eval.forEach(e => appendResult(e, codeBlock));
      }).catch(function(err) {
        console.warn('error from graphql evaluating expression:', expr, err);
      });
      return false;
    };

    // use parentElement because the <code> is wrapped in a <pre>
    codeBlock.parentElement.insertAdjacentElement(
      "afterend", runButton);

    // console.log('yetibot code block', codeBlock, expr);
  });
});


// Bulma Menu JS
document.addEventListener('DOMContentLoaded', function () {
  // Get all "navbar-burger" elements
  var $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);
  // Check if there are any navbar burgers
  if ($navbarBurgers.length > 0) {
    // Add a click event on each of them
    $navbarBurgers.forEach(function ($el) {
      $el.addEventListener('click', function () {
        // Get the target from the "data-target" attribute
        var target = $el.dataset.target;
        var $target = document.getElementById(target);
        // Toggle the class on both the "navbar-burger" and the "navbar-menu"
        $el.classList.toggle('is-active');
        $target.classList.toggle('is-active');
      });
    });
  }
});
