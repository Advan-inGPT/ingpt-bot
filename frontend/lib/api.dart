import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiClient {
  ApiClient({required this.baseUrl});

  final String baseUrl;

  Future<String> chat(String prompt) async {
    final uri = Uri.parse('$baseUrl/chat');
    final res = await http.post(
      uri,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'prompt': prompt}),
    );

    if (res.statusCode >= 200 && res.statusCode < 300) {
      final json = jsonDecode(res.body) as Map<String, dynamic>;
      if (json.containsKey('response')) return json['response'] as String;
      if (json.containsKey('error')) throw json['error'];
      throw 'Unexpected response shape';
    } else {
      throw 'HTTP ${res.statusCode}: ${res.body}';
    }
  }

  Future<String> getCurrentModel() async {
    final uri = Uri.parse('$baseUrl/current_model');
    final res = await http.get(uri);
    final json = jsonDecode(res.body);
    return json['model'];
  }

  Future<void> switchModel(String model) async {
    final uri = Uri.parse('$baseUrl/switch_model');
    final res = await http.post(
      uri,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'model': model}),
    );
    if (res.statusCode >= 300) {
      throw 'Failed to switch model: ${res.body}';
    }
  }
}
