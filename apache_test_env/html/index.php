<!DOCTYPE html>
<!--
To change this license header, choose License Headers in Project Properties.
To change this template file, choose Tools | Templates
and open the template in the editor.
-->
<html lang="en">
    <?php
        include "head.inc.php"
    ?>
    <body>
        <?php 
            include "nav.inc.php"; 
        ?>
        <header class="jumbotron text-center">
            <h1 class="display-4">Welcome to World of Pets!</h1>
            <h2>Home of Singapore's Pet Lovers</h2>
        </header>
        <main class="container">
            <section id="dogs">
                <h2>All About Dogs!</h2>
                <div class="row">
                    <article class="col-sm">
                        <h3>Poodles</h3>
                        <figure>
                            <img class="img-thumbnail poodle" src="images/poodle_small.jpg" alt="Poodle" title="View larger image..."/>
                            <figcaption>Standard Poodle</figcaption>
                        </figure>
                        <p>
                            Poodles are a group of formal dog breeds, the Standard Poodle, Miniature Poodle and Toy Poodle.
                        </p>
                    </article>
                    <article class="col-sm">
                        <h3>Chihuahua</h3>
                        <figure>
                            <img class="img-thumbnail chihuahua" src="images/chihuahua_small.jpg" alt="Chihuahua" title="View larger image..."/>
                            <figcaption>Chihuahua</figcaption>
                        </figure>
                        <p>
                            The Chihuahua is the smallest breed of dog, and is named after the Mexican state of Chihuahua.
                        </p>
                    </article>
                </div>
            </section>
            <section id="cats">
                <h2>All About Cats!</h2>
                <div class="row">
                    <article class="col-sm">
                        <h3>Tabby</h3>
                        <figure>
                            <img class="img-thumbnail tabby" src="images/tabby_small.jpg" alt="Tabby Cat" title="View larger image..."/>
                            <figcaption>Tabby Cat</figcaption>
                        </figure>
                        <p>
                            A tabby is any domestic cat with a distinctive 'M' shaped marking on its forehead, stripes by its eyes and across its cheeks, along its back, and around its legs and tail, and, characteristic striped, dotted, lined, flecked, banded or swirled patterns on the body—neck, shoulders, sides, flanks, chest and abdomen.
                        </p>
                    </article>
                    <article class="col-sm">
                        <h3>Calico</h3>
                        <figure>
                            <img class="img-thumbnail calico" src="images/calico_small.jpg" alt="Calico Cat" title="View larger image..."/>
                            <figcaption>Calico Cat</figcaption>
                        </figure>
                        <p>
                            A calico cat is a domestic cat of any breed with a tri-color coat. The calico cat is most commonly thought of as being typically 25% to 75% white with large orange and black patches (or sometimes cream and grey patches); however, the calico cat can have any three colors in its pattern. They are almost exclusively female except under rare genetic conditions.
                        </p>
                    </article>
                </div>
            </section>
        </main>
        <?php 
            include "footer.inc.php"; 
        ?>
    </body>
</html>