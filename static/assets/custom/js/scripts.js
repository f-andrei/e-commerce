(function () {
    console.log('Hello, this message will be printed in the console!');

    select_variations = document.getElementById('select-variations');
    variation_price = document.getElementById('variation-price');
    variation_price_promotional = document.getElementById('variation-price-promotional');

    if (!select_variations) {
        return;
    }

    if (!variation_price) {
        return;
    }

    select_variations.addEventListener('change', function () {
        price = this.options[this.selectedIndex].getAttribute('data-price');
        price_promotional = this.options[this.selectedIndex].getAttribute('data-price-promotional');

        if (price) {
            variation_price.innerHTML = price;
        }

        if (price_promotional) {
            variation_price_promotional.innerHTML = price_promotional;
        } else {
            variation_price_promotional.innerHTML = price;
            // variation_price.innerHTML = ''; // Optionally clear variation_price if price_promotional doesn't exist
        }
    });
})();
