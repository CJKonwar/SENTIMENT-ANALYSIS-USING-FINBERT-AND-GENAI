<?php

namespace App\Services;

use GuzzleHttp\Client;

class VultrService
{

    private $client;

    public function __construct()
    {
        $this->client = new Client([
            'base_uri' => 'https://api.vultrinference.com/v1/chat/completions',
            'headers' => [
                'Authorization' => 'Bearer ' . 'U4YJTXQ3KIVQIPCVCDUD657Y4YF2RWBCY5LA',
                'Content-Type'  => 'application/json',
            ],
            'verify' => false,  // Disables SSL verification
        ]);
    }


    public function listInstances()
    {
        $response = $this->client->get('instances');
        return json_decode($response->getBody(), true);
    }

    public function getResponse1($userMessage, $collectionId = "aisentify", $modelName = "llama2-13b-chat-Q5_K_M")
    {
        $payload = [
            'collection' => $collectionId,
            'model'       => $modelName,
            'messages'    => [
                [
                    'role'    => 'user',
                    'content' => $userMessage,
                ],
            ],
            'max_tokens'  => 1024,
            'seed'        => -1,
            'temperature' => 0.8,
            'top_k'       => 40,
            'top_p'       => 0.9,
        ];

        $response = $this->client->post('', ['json' => $payload]);

        if ($response->getStatusCode() == 200) {
            $data = json_decode($response->getBody(), true);
            return $data['choices'][0]['message']['content'] ?? 'No response';
        } else {
            return 'Error: ' . $response->getStatusCode() . ' ' . $response->getBody();
        }
    }

    // Function for generating regular responses (optional)
    public function getResponse($userMessage)
    {
        $payload = [
            'model'      => 'llama2-13b-chat-Q5_K_M',
            'messages'   => [
                [
                    'role'    => 'user',
                    'content' => $userMessage,
                ],
            ],
            'max_tokens' => 1000,
            'temperature' => 2,
            'top_k'      => 40,
            'top_p'      => 0.9,
            'stream'     => false,
        ];

        $response = $this->client->post('', ['json' => $payload]);

        if ($response->getStatusCode() == 200) {
            $data = json_decode($response->getBody(), true);
            return $data['choices'][0]['message']['content'] ?? 'No response';
        } else {
            return 'Error: ' . $response->getStatusCode() . ' ' . $response->getBody();
        }
    }
}
