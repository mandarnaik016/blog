var fontawesome = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.9.0/css/all.min.css';
var lora = 'https://fonts.googleapis.com/css?family=Lora:400,700,400italic,700italic&display=swap';
var sans = 'https://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,800italic,400,300,600,700,800&display=swap';

Defer.css(lora, {crossorigin: 'anonymous'}, 0, function() {
    console.info('Lora is loaded!!!');
});

Defer.css(sans, {crossorigin: 'anonymous'}, 0, function() {
    console.info('Sans is loaded!!!');
});

Defer.css(fontawesome, {crossorigin: 'anonymous'}, 0, function() {
    console.info('FontAwesome is loaded!!!');
});