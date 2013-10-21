/**
 * Site wide features
 */
(function($, gettext, ETALAB_VALIDATION_RULES){

    "use strict";

    // Use gettext for validation messages
    $.extend($.validator.messages, {
        required: gettext("This field is required."),
        remote: gettext("Please fix this field."),
        email: gettext("Please enter a valid email address."),
        url: gettext("Please enter a valid URL."),
        date: gettext("Please enter a valid date."),
        dateISO: gettext("Please enter a valid date (ISO)."),
        number: gettext("Please enter a valid number."),
        digits: gettext("Please enter only digits."),
        creditcard: gettext("Please enter a valid credit card number."),
        equalTo: gettext("Please enter the same value again."),
        maxlength: $.validator.format(gettext("Please enter no more than {0} characters.")),
        minlength: $.validator.format(gettext("Please enter at least {0} characters.")),
        rangelength: $.validator.format(gettext("Please enter a value between {0} and {1} characters long.")),
        range: $.validator.format(gettext("Please enter a value between {0} and {1}.")),
        max: $.validator.format(gettext("Please enter a value less than or equal to {0}.")),
        min: $.validator.format(gettext("Please enter a value greater than or equal to {0}."))
    });

    // required: "Ce champ est obligatoire.",
    //     remote: "Veuillez corriger ce champ.",
    //     email: "Veuillez fournir une adresse électronique valide.",
    //     url: "Veuillez fournir une adresse URL valide.",
    //     date: "Veuillez fournir une date valide.",
    //     dateISO: "Veuillez fournir une date valide (ISO).",
    //     number: "Veuillez fournir un numéro valide.",
    //     digits: "Veuillez fournir seulement des chiffres.",
    //     creditcard: "Veuillez fournir un numéro de carte de crédit valide.",
    //     equalTo: "Veuillez fournir encore la même valeur.",
    //     accept: "Veuillez fournir une valeur avec une extension valide.",
    //     maxlength: $.validator.format("Veuillez fournir au plus {0} caractères."),
    //     minlength: $.validator.format("Veuillez fournir au moins {0} caractères."),
    //     rangelength: $.validator.format("Veuillez fournir une valeur qui contient entre {0} et {1} caractères."),
    //     range: $.validator.format("Veuillez fournir une valeur entre {0} et {1}."),
    //     max: $.validator.format("Veuillez fournir une valeur inférieur ou égal à {0}."),
    //     min: $.validator.format("Veuillez fournir une valeur supérieur ou égal à {0}."),
    //     maxWords: $.validator.format("Veuillez fournir au plus {0} mots."),
    //     minWords: $.validator.format("Veuillez fournir au moins {0} mots."),
    //     rangeWords: $.validator.format("Veuillez fournir entre {0} et {1} mots."),
    //     letterswithbasicpunc: "Veuillez fournir seulement des lettres et des signes de ponctuation.",
    //     alphanumeric: "Veuillez fournir seulement des lettres, nombres, espaces et soulignages",
    //     lettersonly: "Veuillez fournir seulement des lettres.",
    //     nowhitespace: "Veuillez ne pas inscrire d'espaces blancs.",
    //     ziprange: "Veuillez fournir un code postal entre 902xx-xxxx et 905-xx-xxxx.",
    //     integer: "Veuillez fournir un nombre non décimal qui est positif ou négatif.",
    //     vinUS: "Veuillez fournir un numéro d'identification du véhicule (VIN).",
    //     dateITA: "Veuillez fournir une date valide.",
    //     time: "Veuillez fournir une heure valide entre 00:00 et 23:59.",
    //     phoneUS: "Veuillez fournir un numéro de téléphone valide.",
    //     phoneUK: "Veuillez fournir un numéro de téléphone valide.",
    //     mobileUK: "Veuillez fournir un numéro de téléphone mobile valide.",
    //     strippedminlength: $.validator.format("Veuillez fournir au moins {0} caractères."),
    //     email2: "Veuillez fournir une adresse électronique valide.",
    //     url2: "Veuillez fournir une adresse URL valide.",
    //     creditcardtypes: "Veuillez fournir un numéro de carte de crédit valide.",
    //     ipv4: "Veuillez fournir une adresse IP v4 valide.",
    //     ipv6: "Veuillez fournir une adresse IP v6 valide.",
    //     require_from_group: "Veuillez fournir au moins {0} de ces champs."


    $(function() {
        // Forms validation
        $('form.validate').validate($.extend({
            // debug: true
        }, ETALAB_VALIDATION_RULES));

        // Form help messages as popover on info sign
        $('.form-help').popover({
            placement: 'top',
            trigger: 'hover',
            html: true
        });

        // Transforme some links into postable forms
        $('a.postable').click(function() {
            var $a = $(this);

            console.log($a.attr('href'));

            $('<form/>', {method: 'post', action: $a.attr('href')})
                .append($('<input/>', {name: $a.data('field-name'), value: $a.data('field-value')}))
                .append($('<input/>', {name: 'csrfmiddlewaretoken', value: $.cookie('csrftoken')}))
                .submit();

            return false;
        });
    });

}(window.jQuery, window.gettext, window.ETALAB_VALIDATION_RULES));
