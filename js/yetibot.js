
const client = graphql("https://public.yetibot.com/graphql");

const yetibotEval = function(expr) {
  const result = client('{eval(expr: "' + expr + '")}')();
  result.then(function(x) {
    console.log(x);
  }).catch(function(err) {
    console.error('error evaluating', expr, err);
  });
  return result;
}

let toc;
let lastScrollY = 0;
const fixedTOCThreshold = 208;

window.addEventListener('scroll', function(e) {
  // add fixed
  if (
    toc &&
    (lastScrollY <= fixedTOCThreshold || !lastScrollY) &&
    window.scrollY > fixedTOCThreshold
  ) {
    // console.log('add fixed', toc);
    toc.classList.add('fixed');
  }

  // remove fixed
  if (
    toc &&
    (lastScrollY >= fixedTOCThreshold || !lastScrollY) &&
    window.scrollY < fixedTOCThreshold
  ) {
    // console.log('remove fixed', toc);
    toc.classList.remove('fixed');
  }

  lastScrollY = window.scrollY;
});


// Either prints raw text or images depending on url structure
const printResponse = (response) => {
}

document.addEventListener('DOMContentLoaded', function () {

  toc = document.querySelector('.toc.column .content');

  if (toc && window.innerWidth > 768) {
    tocbot.init({
      tocSelector: '.toc .content',
      contentSelector: '.page-content',
      // Which headings to grab inside of the contentSelector element.
      headingSelector: 'h1, h2, h3, h4'
    });
  }

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
        console.log(response.eval);
        response.eval.forEach(e => codeBlock.append(e + '\n'));
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
