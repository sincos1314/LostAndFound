// 通用前端交互脚本（登录方式动态可用性、提示等）
document.addEventListener('DOMContentLoaded', () => {
    // 登录页动态控制（仅当页面存在这些元素时）
    const identifierProbeInput = document.querySelector('#identifier-probe');
    const methodTabs = document.querySelectorAll('[data-login-method]');
    const probeButton = document.querySelector('#probe-methods');
    if (identifierProbeInput && probeButton && methodTabs.length) {
      probeButton.addEventListener('click', async () => {
        const val = identifierProbeInput.value.trim();
        if (!val) return;
        try {
          const res = await fetch(`/accounts/login-options/?identifier=${encodeURIComponent(val)}`);
          const data = await res.json();
          methodTabs.forEach(tab => {
            const method = tab.getAttribute('data-login-method');
            if (method === 'email') {
              tab.classList.toggle('disabled', !data.email_exists);
              tab.title = data.email_exists ? '' : '未绑定邮箱，请先使用其他方式登录后在个人中心绑定';
            }
            if (method === 'phone') {
              tab.classList.toggle('disabled', !data.phone_exists);
              tab.title = data.phone_exists ? '' : '未绑定手机号，请先使用其他方式登录后在个人中心绑定';
            }
          });
        } catch(e) {
          console.error(e);
        }
      });
    }
  });