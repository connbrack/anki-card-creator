import os
import subprocess
from pathlib import Path

import boto3
from dotenv import load_dotenv

load_dotenv()


class Polly:
    def __init__(self, client):
        self.client = client

    @staticmethod
    def create_from_env():
        client = boto3.Session(
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('REGION')
        ).client('polly')

        return Polly(client)

    def create_audio(self, text: str, audio_dir: Path, audio_basename: str, tempo: float = 1):

        filepath_fs = audio_dir / f'{audio_basename}_fs.mp3'
        filepath = audio_dir / f'{audio_basename}.mp3'

        tts = self.client.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId='Celine'
        )
        with open(filepath_fs, 'wb') as f:
            f.write(tts['AudioStream'].read())

        if tempo != 1:
            subprocess.run([
                'ffmpeg', '-y', '-i', filepath_fs,
                '-filter:a', f'atempo={tempo}', '-vn', filepath
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
