angular.module('ephox.textboxio').factory('tbioConfigFactory', ['$log',
	function($log) {
		//    $log.log('Loading tbioConfigFactory');
		var configurations = {};

		configurations.default = {
			//        basePath: '/sites/all/libraries/textboxio/resources',
			css: {
				stylesheets: ['/static/css/textboxio.editor.css'],
				styles: [{
					rule: 'p',
					text: 'block.p'
				}, {
					rule: 'h1',
					text: 'block.h1'
				}, {
					rule: 'h2',
					text: 'block.h2'
				}, {
					rule: 'h3',
					text: 'block.h3'
				}, {
					rule: 'h4',
					text: 'block.h4'
				}, {
					rule: 'div',
					text: 'block.div'
				}, {
					rule: 'pre',
					text: 'block.pre'
				}]
			},
			codeview: {
				enabled: true,
				showButton: true
			},
			images: {
				// upload : {},
				allowLocal: true
			},
			languages: ['en', 'es', 'fr', 'de', 'pt', 'zh'],
			// locale : '', // Default locale is inferred from client browser
			paste: {
				style: 'clean'
			},
			// spelling : {},
			ui: {
				toolbar: {
					items: ['undo', 'insert', 'style', 'emphasis', 'align', 'listindent',
						'format', 'tools'
					]
				}
			}
		};

		configurations.simple = {
			//        basePath: '/sites/all/libraries/textboxio/resources',
			css: {
				stylesheets: ['/static/css/app.css'],
				styles: [{
					rule: 'p',
					text: 'block.p'
				}, {
					rule: 'div',
					text: 'block.div'
				}, {
					rule: 'h1',
					text: 'block.h1'
				}, {
					rule: 'h2',
					text: 'block.h2'
				}, {
					rule: 'h3',
					text: 'block.h3'
				}, {
					rule: 'h4',
					text: 'block.h4'
				}]
			},
			codeview: {
				enabled: false,
				showButton: false
			},
			images: {
				// upload : {},
				allowLocal: false
			},
			languages: ['en'],
			// locale : '', // Default locale is inferred from client browser
			paste: {
				style: 'clean'
			},
			// spelling : {},
			ui: {
				toolbar: {
					contextual: [],
					items: ['emphasis', {
						label: 'Table',
						items: ['ul', 'table'],
					}, ]
				}
			}
		};

		return configurations;
	}
]);
