document.addEventListener("DOMContentLoaded", function() {
    const features = [
        {
            id: 1,
            image: "{% static 'images/features/f1.png' %}",
            title: "Free Shipping",
        },
        {
            id: 2,
            image: "{% static 'images/features/f2.png' %}",
            title: "Online Order",
        },
        {
            id: 3,
            image: "{% static 'images/features/f3.png' %}",
            title: "Save Money",
        },
        {
            id: 4,
            image: "{% static 'images/features/f4.png' %}",
            title: "Happy Sell",
        },
        {
            id: 5,
            image: "{% static 'images/features/f5.png' %}",
            title: "F24/7 Support",
        },
        {
            id: 6,
            image: "{% static 'images/features/f6.png' %}",
            title: "Free Shipping",
        },
    ]

    const featureSection = document.getElementById('feature');
    let featuresContent = '';

    features.forEach(feature => {
    const featureContent = `
        <div class="fe-box">
        <img src="${feature.image}" />
        <h6>${feature.title}</h6>
        </div>
    `;
    featuresContent += featureContent;
    });

    if (featureSection) {
    featureSection.innerHTML = featuresContent;
    }
});