import fs from 'fs';

try {
    if (fs.existsSync('dist/index.html')) {
        fs.copyFileSync('dist/index.html', 'dist/404.html');
        console.log('Success: Copied index.html to 404.html for SPA fallback behavior.');
    } else {
        console.warn('Warning: dist/index.html not found. 404.html was not created.');
    }
} catch (error) {
    console.error('Error creating 404.html:', error);
    process.exit(1);
}
