<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Services\VultrService;

class ChatbotController extends Controller
{
    private $vultrService;

    public function __construct(VultrService $vultrService)
    {
        $this->vultrService = $vultrService;
    }

    public function index()
    {
        return view('chatbot.index'); // Ensure this Blade file exists
    }

    public function handleMessage(Request $request)
    {
        $message = $request->input('message');
        
        // Call the VultrService to get a response from the chatbot
        $reply = $this->vultrService->getResponse($message);
        
        // Return the response in JSON format
        return response()->json(['reply' => $reply]);
    }
}


