/**
 * Country visuals shared by every page that draws a flag or a country accent:
 * the programme list, the detail rail and the application calendar.
 *
 * It used to live inside script.js, which only the programmes page loads, so
 * the calendar page could not show a flag without loading the whole
 * programmes controller.
 */
(function () {
    "use strict";

    // CSS-only flag textures keep every country card visually distinct without
    // adding external image requests to the ranked-results view.
    const COUNTRY_VISUALS = {
        austria: { accent: '#ed2939', rgb: '237, 41, 57', flag: 'linear-gradient(to bottom, #ed2939 0 33%, #ffffff 33% 66%, #ed2939 66% 100%)' },
        belgium: { accent: '#f2bd28', rgb: '242, 189, 40', flag: 'linear-gradient(90deg, #191919 0 33%, #f2bd28 33% 66%, #d4303d 66% 100%)' },
        china: { accent: '#e53a3e', rgb: '229, 58, 62', flag: 'radial-gradient(circle at 18% 24%, #ffdf4d 0 3%, transparent 3.5%), #de2910' },
        czechia: { accent: '#d73445', rgb: '215, 52, 69', flag: 'linear-gradient(32deg, #11457e 0 35%, transparent 35.5%), linear-gradient(to bottom, #ffffff 0 50%, #d7141a 50% 100%)' },
        denmark: { accent: '#c8102e', rgb: '200, 16, 46', flag: 'linear-gradient(90deg, transparent 0 29%, #ffffff 29% 40%, transparent 40% 100%), linear-gradient(transparent 0 41%, #ffffff 41% 58%, transparent 58% 100%), #c8102e' },
        estonia: { accent: '#4891d9', rgb: '72, 145, 217', flag: 'linear-gradient(to bottom, #4891d9 0 33%, #17191e 33% 66%, #f7f7f3 66% 100%)' },
        finland: { accent: '#2f70b7', rgb: '47, 112, 183', flag: 'linear-gradient(90deg, transparent 0 30%, #2f70b7 30% 43%, transparent 43% 100%), linear-gradient(transparent 0 40%, #2f70b7 40% 57%, transparent 57% 100%), #f7f7f3' },
        france: { accent: '#2d57a1', rgb: '45, 87, 161', flag: 'linear-gradient(90deg, #21468b 0 33%, #f7f8fa 33% 66%, #ef4135 66% 100%)' },
        germany: { accent: '#d9a620', rgb: '217, 166, 32', flag: 'linear-gradient(to bottom, #1a1a1a 0 33%, #d83232 33% 66%, #e2b42a 66% 100%)' },
        greece: { accent: '#3474bb', rgb: '52, 116, 187', flag: 'linear-gradient(#0d5eaf, #0d5eaf) left top / 42% 56% no-repeat, linear-gradient(90deg, transparent 0 17%, #ffffff 17% 25%, transparent 25%), linear-gradient(transparent 0 23%, #ffffff 23% 33%, transparent 33%), repeating-linear-gradient(to bottom, #0d5eaf 0 11.11%, #ffffff 11.11% 22.22%)' },
        ireland: { accent: '#169b62', rgb: '22, 155, 98', flag: 'linear-gradient(90deg, #169b62 0 33%, #f7f7f3 33% 66%, #ff883e 66% 100%)' },
        italy: { accent: '#159447', rgb: '21, 148, 71', flag: 'linear-gradient(90deg, #009246 0 33%, #f7f8f6 33% 66%, #ce2b37 66% 100%)' },
        japan: { accent: '#dc3044', rgb: '220, 48, 68', flag: 'radial-gradient(circle at 50% 50%, #cf2738 0 22%, transparent 22.5%), #f8f8f4' },
        lithuania: { accent: '#f3b61f', rgb: '243, 182, 31', flag: 'linear-gradient(to bottom, #fdb913 0 33%, #006a44 33% 66%, #c1272d 66% 100%)' },
        netherlands: { accent: '#2d62ad', rgb: '45, 98, 173', flag: 'linear-gradient(to bottom, #ae1c28 0 33%, #f7f8f6 33% 66%, #21468b 66% 100%)' },
        norway: { accent: '#ba0c2f', rgb: '186, 12, 47', flag: 'linear-gradient(90deg, transparent 0 27%, #ffffff 27% 42%, transparent 42%), linear-gradient(transparent 0 38%, #ffffff 38% 62%, transparent 62%), linear-gradient(90deg, transparent 0 31%, #00205b 31% 38%, transparent 38%), linear-gradient(transparent 0 44%, #00205b 44% 56%, transparent 56%), #ba0c2f' },
        poland: { accent: '#d92b48', rgb: '217, 43, 72', flag: 'linear-gradient(to bottom, #fafafa 0 50%, #d22645 50% 100%)' },
        portugal: { accent: '#d84536', rgb: '216, 69, 54', flag: 'radial-gradient(circle at 40% 50%, #f5c242 0 7%, transparent 7.5%), linear-gradient(90deg, #046a38 0 40%, #da291c 40% 100%)' },
        romania: { accent: '#f7c600', rgb: '247, 198, 0', flag: 'linear-gradient(90deg, #002b7f 0 33%, #fcd116 33% 66%, #ce1126 66% 100%)' },
        russia: { accent: '#4366ae', rgb: '67, 102, 174', flag: 'linear-gradient(to bottom, #f7f7f5 0 33%, #3156a6 33% 66%, #ce303c 66% 100%)' },
        south_korea: { accent: '#d43848', rgb: '212, 56, 72', flag: 'radial-gradient(circle at 50% 50%, #cd2e3a 0 12%, #0047a0 12.5% 24%, transparent 24.5%), #ffffff' },
        spain: { accent: '#efb933', rgb: '239, 185, 51', flag: 'linear-gradient(to bottom, #aa151b 0 25%, #f1bf36 25% 75%, #aa151b 75% 100%)' },
        sweden: { accent: '#e4b424', rgb: '228, 180, 36', flag: 'linear-gradient(90deg, transparent 0 29%, #f6cc38 29% 40%, transparent 40% 100%), linear-gradient(transparent 0 40%, #f6cc38 40% 57%, transparent 57% 100%), #2166a5' },
        switzerland: { accent: '#e13c43', rgb: '225, 60, 67', flag: 'linear-gradient(90deg, transparent 0 39%, #fff 39% 61%, transparent 61% 100%), linear-gradient(transparent 0 32%, #fff 32% 68%, transparent 68% 100%), #d52b1e' },
        turkey: { accent: '#e12d3c', rgb: '225, 45, 60', flag: 'radial-gradient(circle at 42% 50%, #e30a17 0 12%, transparent 12.5%), radial-gradient(circle at 36% 50%, #ffffff 0 15%, transparent 15.5%), #e30a17' },
        united_kingdom: { accent: '#c8394d', rgb: '200, 57, 77', flag: 'linear-gradient(27deg, transparent 43%, #cf142b 43% 48%, #ffffff 48% 52%, #cf142b 52% 57%, transparent 57%), linear-gradient(-27deg, transparent 43%, #cf142b 43% 48%, #ffffff 48% 52%, #cf142b 52% 57%, transparent 57%), linear-gradient(90deg, transparent 38%, #ffffff 38% 45%, #cf142b 45% 55%, #ffffff 55% 62%, transparent 62%), linear-gradient(transparent 34%, #ffffff 34% 42%, #cf142b 42% 58%, #ffffff 58% 66%, transparent 66%), #012169' },
        usa: { accent: '#b9334a', rgb: '185, 51, 74', flag: 'linear-gradient(#3c3b6e, #3c3b6e) left top / 42% 54% no-repeat, repeating-linear-gradient(to bottom, #b22234 0 7.69%, #ffffff 7.69% 15.38%)' }
    };

    function countryVisualKey(country) {
        const normalized = String(country || '')
            .trim()
            .toLocaleLowerCase('en-US')
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .replace(/[^a-z0-9]+/g, '_')
            .replace(/^_|_$/g, '');

        return {
            uk: 'united_kingdom',
            great_britain: 'united_kingdom',
            united_states: 'usa',
            united_states_of_america: 'usa',
            america: 'usa',
            czech_republic: 'czechia',
            republic_of_korea: 'south_korea',
            korea_south: 'south_korea',
            korea_republic_of: 'south_korea',
            turkiye: 'turkey'
        }[normalized] || normalized;
    }

    function applyCountryVisual(element, country) {
        if (!element) return;
        const key = countryVisualKey(country);
        const visual = COUNTRY_VISUALS[key] || { accent: '#6f85a2', rgb: '111, 133, 162', flag: 'linear-gradient(135deg, #274261, #162a42)' };
        element.classList.add('country-themed');
        element.dataset.countryTheme = key || 'global';
        element.style.setProperty('--country-accent', visual.accent);
        element.style.setProperty('--country-rgb', visual.rgb);
        element.style.setProperty('--country-flag', visual.flag);
    }

    const COUNTRY_FLAG_CODES = {
        austria: 'AT',
        belgium: 'BE',
        china: 'CN',
        czech_republic: 'CZ',
        czechia: 'CZ',
        denmark: 'DK',
        estonia: 'EE',
        finland: 'FI',
        france: 'FR',
        germany: 'DE',
        greece: 'GR',
        ireland: 'IE',
        italy: 'IT',
        japan: 'JP',
        lithuania: 'LT',
        netherlands: 'NL',
        norway: 'NO',
        poland: 'PL',
        portugal: 'PT',
        romania: 'RO',
        russia: 'RU',
        south_korea: 'KR',
        spain: 'ES',
        sweden: 'SE',
        switzerland: 'CH',
        turkey: 'TR',
        united_kingdom: 'GB',
        usa: 'US'
    };

    function countryFlagCode(country) {
        return COUNTRY_FLAG_CODES[countryVisualKey(country)] || '';
    }

    function countryVisualMeta(country) {
        const key = countryVisualKey(country);
        const visual = COUNTRY_VISUALS[key] || { accent: '#6f85a2', rgb: '111, 133, 162', flag: 'linear-gradient(135deg, #274261, #162a42)' };
        return { key, code: COUNTRY_FLAG_CODES[key] || '', ...visual };
    }

    window.uniCountryVisual = countryVisualMeta;

    window.uniCountryVisualKey = countryVisualKey;
    window.uniCountryFlagCode = countryFlagCode;
    window.uniApplyCountryVisual = applyCountryVisual;
})();
