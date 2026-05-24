package proxy

import (
	"net/http"
	"net/http/httputil"
	"net/url"
)

func ReverseProxy(target string) (*httputil.ReverseProxy, error) {
	urlValue, err := url.Parse(target)
	if err != nil {
		return nil, err
	}

	proxy := httputil.NewSingleHostReverseProxy(urlValue)

	proxy.ModifyResponse = func(resp *http.Response) error {
		resp.Header.Set("X-SovereignBharat", "gateway")
		return nil
	}

	return proxy, nil
}
