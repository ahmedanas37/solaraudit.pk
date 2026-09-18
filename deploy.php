<?php
/**
 * Automated Deployment Webhook for solaraudit.online
 * Triggers instant git synchronization whenever code is pushed to GitHub.
 */

// Deployment secret key (matches GitHub webhook secret)
$secret = 'solaraudit_deploy_2026';

// 1. Verify Authentication
$authenticated = false;

// Method A: Query parameter (?secret=solaraudit_deploy_2026)
if (isset($_GET['secret']) && hash_equals($secret, (string)$_GET['secret'])) {
    $authenticated = true;
}

// Method B: GitHub Webhook signature header (X-Hub-Signature-256)
$signature = $_SERVER['HTTP_X_HUB_SIGNATURE_256'] ?? '';
$raw_payload = file_get_contents('php://input');

if (!$authenticated && !empty($signature) && !empty($raw_payload)) {
    $expected_signature = 'sha256=' . hash_hmac('sha256', $raw_payload, $secret);
    if (hash_equals($expected_signature, $signature)) {
        $authenticated = true;
    }
}

if (!$authenticated) {
    http_response_code(403);
    header('Content-Type: text/plain; charset=utf-8');
    echo "403 Forbidden: Invalid or missing deployment secret.\n";
    exit;
}

// 2. Deployment Execution
$repo_dir = '/home/zynk/solaraudit.online';

// Ensure Git uses safe directory settings and clean reset to avoid merge conflicts
$commands = [
    "cd {$repo_dir}",
    "git config --global --add safe.directory {$repo_dir} 2>&1",
    "git fetch origin master 2>&1",
    "git reset --hard origin/master 2>&1"
];

// Optional: also trigger cPanel deployment task if uapi is accessible
$uapi_bin = '/usr/local/cpanel/bin/uapi';
if (file_exists($uapi_bin)) {
    $commands[] = "{$uapi_bin} VersionControl deployment create repository_root={$repo_dir} 2>&1";
}

$full_cmd = implode(' && ', $commands);
$output = [];
$return_code = 0;

if (function_exists('exec')) {
    exec($full_cmd, $output, $return_code);
} elseif (function_exists('shell_exec')) {
    $res = shell_exec($full_cmd);
    $output = explode("\n", (string)$res);
    $return_code = 0;
} else {
    http_response_code(500);
    header('Content-Type: text/plain; charset=utf-8');
    echo "500 Server Error: Both exec() and shell_exec() are disabled on this PHP host.\n";
    echo "Recommendation: Use cPanel Cron Job instead.\n";
    exit;
}

header('Content-Type: text/plain; charset=utf-8');
echo "=== SolarAudit Auto-Deploy Log ===\n";
echo "Timestamp: " . date('Y-m-d H:i:s T') . "\n";
echo "Status: " . ($return_code === 0 ? "SUCCESS" : "FAILED (code $return_code)") . "\n";
echo "Output:\n" . implode("\n", $output) . "\n";
